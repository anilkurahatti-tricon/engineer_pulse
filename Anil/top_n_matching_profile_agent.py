"""
Top-N Employee Profile Matching Agent (RAG + LangChain + Groq)
---------------------------------------------------------------
Given a project's Job Description (JD), this agent finds the top-N existing
employees whose skills/projects/bio best match the JD, and asks a Groq LLM
to produce a ranked, explainable shortlist.

Why RAG (and not "just ask the LLM")?
- The employee pool can be large (hundreds/thousands of profiles). Stuffing
  every profile into the LLM prompt does not scale on cost, latency, or the
  model's context window, and irrelevant profiles dilute the LLM's attention.
- RAG solves this with a two-stage pipeline:
    1) RETRIEVAL (cheap, scalable): embed the JD once, then use vector
       similarity (cosine distance) to pull only the top-K most plausible
       candidates out of the full employee base. This is where pgvector fits:
       employee skill/project text is embedded once (offline) and stored in
       Postgres; at query time we run a single ANN/HNSW similarity query
       (`embedding <=> jd_embedding`) instead of scanning everything.
    2) GENERATION / RE-RANKING (expensive, smart): only the shortlisted K
       candidates (e.g. 10-15) are handed to the Groq LLM together with the
       JD. The LLM does the nuanced reasoning that pure vector similarity
       can't (weighing seniority, must-have vs nice-to-have skills, gaps)
       and returns the final top-N with a match score and justification.
- This module implements both stages:
    - Stage 1 (retrieval) has two interchangeable backends:
        a) In-memory cosine similarity over `SAMPLE_EMPLOYEES` (no DB needed,
           good for local dev/demo).
        b) Postgres + pgvector (`retrieve_top_candidates_pgvector`), reusing
           the same `employees` / `employee_skills` / `employee_projects`
           tables and HNSW indexes created by
           `backend/scripts/setup_postgres_vector.py`. Enable it by setting
           DATABASE_URL (or POSTGRES_* vars) and USE_PGVECTOR=true in .env.
    - Stage 2 (generation) is the same LangChain `prompt | ChatGroq | parser`
      chain pattern used by `employee_gap_analysis_agent.py`.

Extensibility points:
- `EmployeeProfile` / `JobRequirement` dataclasses can grow new fields.
- `SAMPLE_EMPLOYEES` is just a list -> swap for real data without touching
  the retrieval/generation logic.
- `embed_text()` isolates the embedding provider (a deterministic offline
  fallback, since only GROQ_API_KEY is available — no separate embeddings
  API key) so a real embedding provider can be swapped in later if needed.
- `run_top_n_match()` is the single reusable entry point other modules
  (e.g. a FastAPI controller) can call.
"""

import json
import math
import os
import random
from dataclasses import asdict, dataclass, field
from typing import List, Optional, Tuple

import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

dotenv.load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Must match the dimension used by backend/scripts/setup_postgres_vector.py
# so vectors stay comparable if this agent is pointed at the same Postgres DB.
EMBEDDING_DIMENSION = 1536


# --------------------------------------------------------------------------
# Domain models
# --------------------------------------------------------------------------
@dataclass
class JobRequirement:
    project_name: str
    description: str
    required_skills: List[str]
    nice_to_have_skills: List[str] = field(default_factory=list)

    def as_text(self) -> str:
        """Flattened text used to compute the JD embedding."""
        parts = [self.project_name, self.description,
                  "Required skills: " + ", ".join(self.required_skills)]
        if self.nice_to_have_skills:
            parts.append("Nice to have: " + ", ".join(self.nice_to_have_skills))
        return "\n".join(parts)


@dataclass
class EmployeeProfile:
    employee_id: int
    name: str
    title: str
    skills: List[str]
    years_experience: float
    projects_summary: str
    bio: str = ""

    def as_text(self) -> str:
        """Flattened text used to compute the employee's embedding."""
        return (
            f"{self.title} with {self.years_experience} years experience. "
            f"Skills: {', '.join(self.skills)}. "
            f"Projects: {self.projects_summary}. {self.bio}"
        )


# --------------------------------------------------------------------------
# Sample data (replace with real data loaded from Postgres in production)
# --------------------------------------------------------------------------
SAMPLE_EMPLOYEES: List[EmployeeProfile] = [
    EmployeeProfile(
        employee_id=1, name="Jane Doe", title="Senior Backend Engineer",
        skills=["Python", "FastAPI", "PostgreSQL", "Docker", "Async APIs"],
        years_experience=6.0,
        projects_summary="Designed and built the Engineer Pulse FastAPI backend with layered architecture.",
        bio="Specializes in high-throughput FastAPI microservices and async Python APIs.",
    ),
    EmployeeProfile(
        employee_id=2, name="John Smith", title="Frontend Engineer",
        skills=["React", "TypeScript", "Vite", "Material UI"],
        years_experience=4.0,
        projects_summary="Built the Engineer Pulse React frontend including dashboards and charts.",
        bio="Builds React component libraries and performance-optimized UIs.",
    ),
    EmployeeProfile(
        employee_id=3, name="Alex Lee", title="Full-Stack Engineer",
        skills=["FastAPI", "React", "OpenAI API", "Microservices"],
        years_experience=5.0,
        projects_summary="Integrated an Azure OpenAI chatbot backend with streaming and session history.",
        bio="Experienced in both FastAPI backend and React frontend with a DevOps mindset.",
    ),
    EmployeeProfile(
        employee_id=4, name="Priya Sharma", title="Data & AI Engineer",
        skills=["PostgreSQL", "pgvector", "Machine Learning", "Embeddings", "Python"],
        years_experience=7.0,
        projects_summary="Designed the vector embedding pipeline and HNSW index strategy for sub-100ms cosine search.",
        bio="Expert in PostgreSQL, pgvector, and ML pipeline architecture.",
    ),
    EmployeeProfile(
        employee_id=5, name="Carlos Rodriguez", title="DevOps Engineer",
        skills=["Docker", "Kubernetes", "CI/CD", "GitHub Actions"],
        years_experience=5.5,
        projects_summary="Set up Docker Compose for local dev and CI/CD pipelines for automated deployment.",
        bio="Manages Docker, Kubernetes clusters, and CI/CD pipelines at scale.",
    ),
    EmployeeProfile(
        employee_id=6, name="Meera Nair", title="Backend Engineer",
        skills=["Node.js", "Express", "MongoDB", "REST API design"],
        years_experience=3.5,
        projects_summary="Built REST APIs for an internal order-management tool.",
        bio="Comfortable across JavaScript backend stacks and NoSQL data modeling.",
    ),
    EmployeeProfile(
        employee_id=7, name="David Chen", title=".NET Engineer",
        skills=["ASP.NET Core", "Azure", "SQL Server", "C#"],
        years_experience=4.5,
        projects_summary="Rebuilt a legacy customer portal on ASP.NET Core Web API and Azure App Service.",
        bio="Focused on enterprise .NET services and Azure cloud deployments.",
    ),
    EmployeeProfile(
        employee_id=8, name="Sara Khan", title="ML Engineer",
        skills=["Python", "PyTorch", "Vector Databases", "NLP", "Embeddings"],
        years_experience=4.0,
        projects_summary="Built an NLP-based semantic search prototype using vector similarity search.",
        bio="Passionate about applied ML and retrieval-augmented systems.",
    ),
]

SAMPLE_JD = JobRequirement(
    project_name="AI-Powered Talent Search Platform",
    description=(
        "Build a semantic search service that embeds job descriptions and employee "
        "profiles, stores vectors in PostgreSQL, and exposes a FastAPI endpoint that "
        "returns ranked candidate matches for a given project."
    ),
    required_skills=["Python", "FastAPI", "PostgreSQL", "pgvector", "Machine Learning / Embeddings"],
    nice_to_have_skills=["Docker", "OpenAI API"],
)


# --------------------------------------------------------------------------
# Stage 1a: Embeddings
# --------------------------------------------------------------------------
def _deterministic_embedding(text: str, dimension: int = EMBEDDING_DIMENSION) -> List[float]:
    """Reproducible unit-normalized pseudo-embedding (no external embeddings API key needed).

    Kept identical to backend/scripts/setup_postgres_vector.py's fallback so
    vectors stay comparable if this agent is later pointed at the same DB.
    """
    rng = random.Random(hash(text) % (2**31))
    vec = [rng.gauss(0, 1) for _ in range(dimension)]
    magnitude = math.sqrt(sum(x * x for x in vec))
    return [x / magnitude for x in vec]


def embed_text(text: str) -> List[float]:
    """Get an embedding. Deterministic offline fallback only — we only have GROQ_API_KEY,
    no separate embeddings provider key. Swap in a real embedding call here if one becomes available.
    """
    return _deterministic_embedding(text)


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# --------------------------------------------------------------------------
# Stage 1b: Retrieval (the "R" in RAG)
# --------------------------------------------------------------------------
def retrieve_top_candidates_in_memory(
    jd_embedding: List[float],
    employees: List[EmployeeProfile],
    top_k: int = 10,
) -> List[Tuple[EmployeeProfile, float]]:
    """Rank employees by cosine similarity to the JD embedding, no DB required."""
    scored = [(emp, _cosine_similarity(jd_embedding, embed_text(emp.as_text()))) for emp in employees]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]


def retrieve_top_candidates_pgvector(
    jd_embedding: List[float],
    top_k: int = 10,
) -> Optional[List[Tuple[EmployeeProfile, float]]]:
    """Retrieve candidates via a Postgres + pgvector ANN query.

    Reuses the `employees` / `employee_skills` / `employee_projects` tables
    and HNSW indexes created by backend/scripts/setup_postgres_vector.py.
    Returns None (so callers fall back to in-memory mode) if psycopg2 isn't
    installed or the DB isn't reachable — this keeps the script runnable
    without any DB setup.
    """
    try:
        import psycopg2
        from pgvector.psycopg2 import register_vector
    except ImportError:
        return None

    dsn = os.getenv("DATABASE_URL") or (
        f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
        f"port={os.getenv('POSTGRES_PORT', '5432')} "
        f"dbname={os.getenv('POSTGRES_DB', 'engineer_pulse')} "
        f"user={os.getenv('POSTGRES_USER', 'postgres')} "
        f"password={os.getenv('POSTGRES_PASSWORD', 'postgres')}"
    )

    try:
        conn = psycopg2.connect(dsn)
    except Exception:
        return None

    try:
        register_vector(conn)
        with conn.cursor() as cur:
            # Nearest-neighbor search on employee_skills embeddings (cosine distance <=>),
            # aggregated to the best (closest) match per employee.
            cur.execute(
                """
                SELECT e.id, e.name, e.title, e.total_experience_years, e.bio,
                       MIN(s.embedding <=> %s::vector) AS distance
                FROM employees e
                JOIN employee_skills s ON s.employee_id = e.id
                GROUP BY e.id, e.name, e.title, e.total_experience_years, e.bio
                ORDER BY distance ASC
                LIMIT %s;
                """,
                (jd_embedding, top_k),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    results: List[Tuple[EmployeeProfile, float]] = []
    for emp_id, name, title, exp_years, bio, distance in rows:
        profile = EmployeeProfile(
            employee_id=emp_id, name=name, title=title, skills=[],
            years_experience=float(exp_years or 0), projects_summary="", bio=bio or "",
        )
        results.append((profile, 1 - distance))  # convert cosine distance -> similarity
    return results


def retrieve_top_candidates(
    jd: JobRequirement,
    employees: Optional[List[EmployeeProfile]] = None,
    top_k: int = 10,
    use_pgvector: bool = False,
) -> List[Tuple[EmployeeProfile, float]]:
    """Single retrieval entry point: tries pgvector first (if requested), else in-memory."""
    jd_embedding = embed_text(jd.as_text())
    if use_pgvector:
        pgvector_results = retrieve_top_candidates_pgvector(jd_embedding, top_k)
        if pgvector_results is not None:
            return pgvector_results
    return retrieve_top_candidates_in_memory(jd_embedding, employees or SAMPLE_EMPLOYEES, top_k)


# --------------------------------------------------------------------------
# Stage 2: Generation / re-ranking with Groq (the "G" in RAG)
# --------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert Technical Recruiter and Talent-Matching Specialist.
You receive a project Job Description (JD) and a shortlist of candidate employees
that have already been narrowed down by vector similarity search. Your job is to
apply nuanced judgment (seniority, must-have vs nice-to-have skills, real project
experience) to select and rank the best matches.

Rules:
- Base your analysis only on the JD and candidate data provided in the user message.
- Only select candidates from the provided shortlist; never invent employees.
- Rank strictly by overall fit for the JD, best first.
- "match_score" is an integer 0-100 estimating overall fit.
- "matched_skills" are required/nice-to-have JD skills the candidate already has.
- "missing_skills" are required JD skills the candidate does NOT have.
- Respond with ONLY valid JSON (no markdown fences, no commentary) matching EXACTLY this structure:

{{
  "project_name": "string",
  "top_matches": [
    {{
      "employee_id": number,
      "name": "string",
      "match_score": number,
      "matched_skills": ["string"],
      "missing_skills": ["string"],
      "reasoning": "string"
    }}
  ]
}}"""


def _format_user_prompt(
    jd: JobRequirement,
    candidates: List[Tuple[EmployeeProfile, float]],
    top_n: int,
) -> str:
    """Builds the user-turn content sent to the LLM from the retrieved shortlist."""
    payload = {
        "job_requirement": asdict(jd),
        "top_n_requested": top_n,
        "candidate_shortlist": [
            {**asdict(emp), "retrieval_similarity_score": round(score, 4)}
            for emp, score in candidates
        ],
    }
    return (
        f"From the candidate_shortlist below (already pre-filtered by vector search), "
        f"select and rank the top {top_n} best matches for the job_requirement. "
        "Return the JSON described in the system prompt.\n\n"
        f"{json.dumps(payload, indent=2)}"
    )


def build_chain(model: str = GROQ_MODEL, temperature: float = 0.3):
    """Wires up the LangChain prompt | LLM | parser pipeline. Swap model/parser here."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your .env file before running the agent."
        )

    llm = ChatGroq(api_key=api_key, model=model, temperature=temperature)
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("user", "{input}"),
        ]
    )
    return prompt | llm | parser


def run_top_n_match(
    jd: JobRequirement,
    employees: Optional[List[EmployeeProfile]] = None,
    top_n: int = 5,
    retrieval_k: int = 10,
    use_pgvector: bool = False,
    chain=None,
) -> dict:
    """Single reusable entry point: retrieval (pgvector or in-memory) + LLM re-ranking."""
    candidates = retrieve_top_candidates(jd, employees, top_k=retrieval_k, use_pgvector=use_pgvector)
    chain = chain or build_chain()
    user_input = _format_user_prompt(jd, candidates, top_n)
    return chain.invoke({"input": user_input})


def _prompt_for_jd_override(default: JobRequirement) -> JobRequirement:
    """Optional interactive override of the sample JD (press Enter to accept defaults)."""
    print("\nUsing sample JD. Press Enter to accept the default, or type a new value.")
    project_name = input(f"Project name [{default.project_name}]: ").strip() or default.project_name
    description = input(f"Description [{default.description}]: ").strip() or default.description
    skills_raw = input(
        f"Required skills, comma-separated [{', '.join(default.required_skills)}]: "
    ).strip()
    required_skills = [s.strip() for s in skills_raw.split(",")] if skills_raw else default.required_skills
    return JobRequirement(
        project_name=project_name,
        description=description,
        required_skills=required_skills,
        nice_to_have_skills=default.nice_to_have_skills,
    )


if __name__ == "__main__":
    try:
        jd = _prompt_for_jd_override(SAMPLE_JD)
        use_pgvector = os.getenv("USE_PGVECTOR", "false").lower() == "true"
        result = run_top_n_match(jd, top_n=5, use_pgvector=use_pgvector)
        print("\n--- Top-N Match JSON (for UI consumption) ---")
        print(json.dumps(result, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
