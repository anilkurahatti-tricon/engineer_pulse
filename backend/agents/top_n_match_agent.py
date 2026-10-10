"""
Top-N Employee-Project Match Agent
-----------------------------------
Single-file, extensible LangChain + Groq agent that takes one target project
and a pool of employees, scores every employee's readiness for that project
using the same methodology as the gap-analysis agent (0-100 readiness score),
and returns the top N employees ordered by score descending.

Reuses the `Employee` / `ProjectRequirement` dataclasses from
`gap_analysis_agent` so the employee-skills and project-skill shapes stay
identical across both agents.

Extensibility points:
- `SAMPLE_EMPLOYEES` / `SAMPLE_PROJECTS_BY_ID` are just data -> swap for a real
  DB-backed list without touching the agent logic.
- `build_chain()` isolates the LLM/prompt wiring so the model or parser can be swapped independently.
- `run_top_n_match()` is the single reusable entry point other modules (e.g. a FastAPI controller) can call.
"""

import json
import os
from dataclasses import asdict
from typing import List, Tuple

import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from agents.gap_analysis_agent import Employee, ProjectRequirement

dotenv.load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


# --------------------------------------------------------------------------
# Sample data (used only when the DB has no matching project/employees)
# --------------------------------------------------------------------------
SAMPLE_EMPLOYEES: List[Employee] = [
    Employee(employee_id=1, name="Jane Doe", experience_years=6.0, role="Senior Backend Engineer",
             current_skills=["Python", "FastAPI", "PostgreSQL", "Docker", "REST API design"]),
    Employee(employee_id=2, name="John Smith", experience_years=4.0, role="Frontend Engineer",
             current_skills=["React", "TypeScript", "Vite", "Material UI"]),
    Employee(employee_id=3, name="Alex Lee", experience_years=5.0, role="Full-Stack Engineer",
             current_skills=["FastAPI", "React", "OpenAI API", "Microservices", "Docker"]),
    Employee(employee_id=4, name="Priya Sharma", experience_years=7.0, role="Data & AI Engineer",
             current_skills=["PostgreSQL", "pgvector", "Machine Learning", "Embeddings", "Python"]),
    Employee(employee_id=5, name="Carlos Rodriguez", experience_years=5.5, role="DevOps Engineer",
             current_skills=["Docker", "Kubernetes", "CI/CD", "GitHub Actions"]),
    Employee(employee_id=6, name="Meera Nair", experience_years=3.5, role="Backend Engineer",
             current_skills=["Node.js", "Express", "MongoDB", "REST API design"]),
    Employee(employee_id=7, name="David Chen", experience_years=4.5, role=".NET Engineer",
             current_skills=["ASP.NET Core", "Azure", "SQL Server", "C#"]),
    Employee(employee_id=8, name="Sara Khan", experience_years=4.0, role="ML Engineer",
             current_skills=["Python", "PyTorch", "Vector Databases", "NLP", "Embeddings"]),
]

SAMPLE_PROJECTS_BY_ID: dict[int, ProjectRequirement] = {
    1: ProjectRequirement(
        project_id=1,
        project_name="Customer Portal Modernization",
        description=(
            "Rebuild a legacy customer portal as an ASP.NET Core Web API backend "
            "with a REST API layer and an Angular single-page frontend."
        ),
        required_skills=[
            "ASP.NET Core Web API", "REST API design", "Entity Framework Core",
            "Angular", "JWT Authentication", "Azure App Service", "Docker",
            "xUnit", "Azure DevOps CI/CD", "SQL Server",
        ],
        tech_stack_summary=".NET 8 Web API + Angular + Azure",
    ),
    2: ProjectRequirement(
        project_id=2,
        project_name="AI-Powered Talent Search Platform",
        description=(
            "Build a semantic search service that embeds job descriptions and employee "
            "profiles, stores vectors in PostgreSQL, and exposes a FastAPI endpoint that "
            "returns ranked candidate matches for a given project."
        ),
        required_skills=["Python", "FastAPI", "PostgreSQL", "pgvector", "Machine Learning", "Embeddings"],
        tech_stack_summary="FastAPI + PostgreSQL/pgvector + Python ML",
    ),
    3: ProjectRequirement(
        project_id=3,
        project_name="Inventory Management Microservices Platform",
        description=(
            "A distributed inventory system built as independent .NET microservices "
            "communicating over REST and messaging queues, deployed on Kubernetes."
        ),
        required_skills=[
            ".NET Microservices", "REST API design", "RabbitMQ", "Docker",
            "Kubernetes", "gRPC", "PostgreSQL", "React", "GitHub Actions CI/CD",
        ],
        tech_stack_summary=".NET Microservices + Docker/Kubernetes + React",
    ),
}


def sample_project_for_id(project_id: int) -> ProjectRequirement:
    """Deterministic fallback project so any project_id still yields a usable demo result."""
    if project_id in SAMPLE_PROJECTS_BY_ID:
        return SAMPLE_PROJECTS_BY_ID[project_id]
    ids = sorted(SAMPLE_PROJECTS_BY_ID)
    fallback = SAMPLE_PROJECTS_BY_ID[ids[project_id % len(ids)]]
    return ProjectRequirement(
        project_id=project_id,
        project_name=fallback.project_name,
        description=fallback.description,
        required_skills=fallback.required_skills,
        tech_stack_summary=fallback.tech_stack_summary,
    )


# --------------------------------------------------------------------------
# Deterministic skill matching (never left to the LLM to avoid score/matched-skills drift)
# --------------------------------------------------------------------------
def _normalize(skill: str) -> str:
    return skill.strip().lower()


def _skills_overlap(required_skill: str, current_skill: str) -> bool:
    """Case-insensitive exact or substring match, e.g. "Docker" <-> "Docker Compose"."""
    required, current = _normalize(required_skill), _normalize(current_skill)
    return required == current or required in current or current in required


def compute_skill_match(required_skills: List[str], current_skills: List[str]) -> Tuple[List[str], List[str]]:
    """Deterministically splits required_skills into matched/missing against current_skills.

    Computed in Python (not by the LLM) so "matched_skills" always agrees with the raw
    skill lists, and the readiness score can be reliably anchored to it.
    """
    matched = [req for req in required_skills if any(_skills_overlap(req, cur) for cur in current_skills)]
    missing = [req for req in required_skills if req not in matched]
    return matched, missing


# --------------------------------------------------------------------------
# Prompt
# --------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert Technical Career Coach and Talent-Matching Analyst.
You score EVERY employee's readiness for ONE target project, using the same methodology a
skills-gap analysis would use.

Each employee in the input already includes precomputed "matched_skills" and
"missing_skills" (exact overlap between the employee's current skills and the project's
required skills) plus a "skill_match_ratio" (matched / total required skills). These are
ground truth - you MUST return them back unchanged in your output, never recompute or alter them.

Rules:
- Base your analysis only on the project and employee data provided in the user message.
- You MUST score every single employee in the input list - never omit one.
- "overall_readiness_score" is an integer 0-100. It MUST be driven primarily by
  "skill_match_ratio": if skill_match_ratio is 0 (no matched skills at all), the score MUST
  be 0 regardless of experience or role. Otherwise, scale the score with skill_match_ratio
  and use experience_years / role relevance only as a secondary modifier (+/- a few points).
- Return the employee's "matched_skills" and "missing_skills" exactly as given in the input.
- Respond with ONLY valid JSON (no markdown fences, no commentary) matching EXACTLY this structure:

{{
  "project_name": "string",
  "required_skills": ["string"],
  "candidates": [
    {{
      "employee_name": "string",
      "experience_years": number,
      "overall_readiness_score": number,
      "matched_skills": ["string"],
      "missing_skills": ["string"]
    }}
  ]
}}"""


def _format_user_prompt(project: ProjectRequirement, employees: List[Employee]) -> str:
    """Builds the user-turn content sent to the LLM, with skill matches precomputed per employee."""
    employees_payload = []
    for employee in employees:
        matched, missing = compute_skill_match(project.required_skills, employee.current_skills)
        employee_payload = asdict(employee)
        employee_payload["matched_skills"] = matched
        employee_payload["missing_skills"] = missing
        employee_payload["skill_match_ratio"] = (
            round(len(matched) / len(project.required_skills), 2) if project.required_skills else 0.0
        )
        employees_payload.append(employee_payload)

    payload = {"project": asdict(project), "employees": employees_payload}
    return (
        "Score every employee below against the target project and return the JSON "
        "described in the system prompt.\n\n"
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
    project: ProjectRequirement,
    employees: List[Employee],
    top_n: int,
    chain=None,
) -> dict:
    """Single reusable entry point: scores all employees, then returns the top N as a JSON-ready dict."""
    chain = chain or build_chain()
    user_input = _format_user_prompt(project, employees)
    result = chain.invoke({"input": user_input})

    # Re-derive matched/missing skills and re-anchor the score ourselves - never trust the
    # LLM's own copy, since it can drift from the ground-truth skill overlap (e.g. report a
    # non-zero score with an empty matched_skills list).
    employees_by_name = {e.name: e for e in employees}
    candidates = result.get("candidates", [])
    for candidate in candidates:
        employee = employees_by_name.get(candidate.get("employee_name"))
        if employee is None:
            continue
        matched, missing = compute_skill_match(project.required_skills, employee.current_skills)
        candidate["matched_skills"] = matched
        candidate["missing_skills"] = missing
        if not matched:
            candidate["overall_readiness_score"] = 0
        else:
            candidate["overall_readiness_score"] = max(0, min(100, candidate.get("overall_readiness_score", 0)))

    # Map scored candidates back to employee_id by name so API consumers can link to a profile.
    employee_id_by_name = {e.name: e.employee_id for e in employees}
    candidates.sort(key=lambda c: c.get("overall_readiness_score", 0), reverse=True)
    top_candidates = candidates[: max(top_n, 0)]
    for rank, candidate in enumerate(top_candidates, start=1):
        candidate["rank"] = rank
        candidate["employee_id"] = employee_id_by_name.get(candidate.get("employee_name"))

    return {
        "project_id": project.project_id,
        "project_name": result.get("project_name", project.project_name),
        "required_skills": result.get("required_skills", project.required_skills),
        "top_n": top_n,
        "employees": top_candidates,
    }


if __name__ == "__main__":
    try:
        project = SAMPLE_PROJECTS_BY_ID[1]
        result = run_top_n_match(project, SAMPLE_EMPLOYEES, top_n=5)
        print("\n--- Top-N Employee Match JSON (for UI consumption) ---")
        print(json.dumps(result, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
