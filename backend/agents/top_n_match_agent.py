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
             current_skills=["Python & FastAPI", "PostgreSQL", "Docker", "REST API design"]),
    Employee(employee_id=2, name="John Smith", experience_years=4.0, role="Frontend Engineer",
             current_skills=["React & Frontend Architecture", "TypeScript", "Vite", "Material UI & Styling"]),
    Employee(employee_id=3, name="Alex Lee", experience_years=5.0, role="Full-Stack Engineer",
             current_skills=["FastAPI & Microservices", "React & State Management", "OpenAI API", "Docker"]),
    Employee(employee_id=4, name="Priya Sharma", experience_years=7.0, role="Data & AI Engineer",
             current_skills=["PostgreSQL & pgvector Search", "Machine Learning & Embeddings", "Python & Data Science"]),
    Employee(employee_id=5, name="Carlos Rodriguez", experience_years=5.5, role="DevOps Engineer",
             current_skills=["Docker, Kubernetes & CI/CD", "Azure DevOps & GitHub Actions"]),
    Employee(employee_id=6, name="Meera Nair", experience_years=8.0, role="Cloud Solutions Architect",
             current_skills=["AWS Cloud Architecture", "Terraform (IaC)", "Kubernetes", "Microservices Design"]),
    Employee(employee_id=7, name="David Chen", experience_years=6.5, role="Senior .NET Engineer",
             current_skills=["ASP.NET Core Web API", "C# & .NET 8", "SQL Server & Entity Framework Core"]),
    Employee(employee_id=8, name="Sara Khan", experience_years=4.5, role="Machine Learning Specialist",
             current_skills=["Python & PyTorch", "Vector Databases & RAG", "Natural Language Processing"]),
    Employee(employee_id=9, name="Marcus Johnson", experience_years=5.5, role="Security & Compliance Lead",
             current_skills=["OAuth2 / OpenID Connect", "OWASP Security & Penetration Testing", "JWT Authentication"]),
    Employee(employee_id=10, name="Elena Rostova", experience_years=5.0, role="Senior Frontend Engineer",
             current_skills=["React & Modern Hooks", "TypeScript", "Web Performance Optimization", "Material UI & Styling"]),
    Employee(employee_id=11, name="Rohan Patel", experience_years=6.0, role="Data Platform Engineer",
             current_skills=["Apache Kafka & Event Streaming", "Apache Spark & Data Pipelines", "PostgreSQL"]),
    Employee(employee_id=12, name="Sophie Martin", experience_years=4.0, role="Mobile Solutions Engineer",
             current_skills=["React Native", "GraphQL", "Mobile CI/CD", "TypeScript"]),
    Employee(employee_id=13, name="Liam O'Connor", experience_years=5.0, role="Site Reliability Engineer",
             current_skills=["Kubernetes & Container Orchestration", "Prometheus & Grafana Observability", "Terraform (IaC)"]),
    Employee(employee_id=14, name="Ananya Joshi", experience_years=4.5, role="QA Automation Lead",
             current_skills=["Playwright & Cypress Testing", "CI/CD Test Automation", "PyTest"]),
    Employee(employee_id=15, name="Tyler Brooks", experience_years=7.5, role="Distributed Systems Architect",
             current_skills=["Go (Golang)", "gRPC & Protobuf", "Redis caching & Messaging", "PostgreSQL"]),
]

SAMPLE_PROJECTS_BY_ID: dict[int, ProjectRequirement] = {
    1: ProjectRequirement(
        project_id=1,
        project_name="Engineer Pulse API",
        description="Designed and built the entire FastAPI backend with layered architecture and AI-powered search.",
        required_skills=["FastAPI", "PostgreSQL", "pgvector", "Docker"],
        tech_stack_summary="FastAPI + PostgreSQL + pgvector + Docker",
    ),
    2: ProjectRequirement(
        project_id=2,
        project_name="Engineer Pulse Frontend",
        description="Built the React frontend including dashboard charts, feedback forms, and chatbot interface.",
        required_skills=["React", "Vite", "Material UI", "Recharts"],
        tech_stack_summary="React + Vite + Material UI",
    ),
    3: ProjectRequirement(
        project_id=3,
        project_name="Customer Portal Modernization",
        description="Rebuild legacy customer portal as an ASP.NET Core Web API backend with a REST API layer and modern Angular single-page frontend.",
        required_skills=["ASP.NET Core Web API", "REST API design", "Angular", "SQL Server", "Docker", "Azure App Service"],
        tech_stack_summary=".NET 8 Web API + Angular + Azure",
    ),
    4: ProjectRequirement(
        project_id=4,
        project_name="Inventory Management Microservices Platform",
        description="Distributed inventory management architecture built with resilient event-driven microservices communicating over RabbitMQ queues.",
        required_skills=[".NET Microservices", "RabbitMQ", "Docker", "Kubernetes", "gRPC", "PostgreSQL", "React"],
        tech_stack_summary=".NET Microservices + Docker/Kubernetes + React",
    ),
    5: ProjectRequirement(
        project_id=5,
        project_name="Real-Time Event Streaming Pipeline",
        description="Engineered real-time telemetry streaming backbone processing high-volume sensor metrics with Kafka and Redis.",
        required_skills=["Apache Kafka", "Python", "PostgreSQL", "Docker", "Redis"],
        tech_stack_summary="Apache Kafka + Python + Redis + PostgreSQL",
    ),
    6: ProjectRequirement(
        project_id=6,
        project_name="Cloud Migration & Multi-Region Kubernetes",
        description="Led zero-downtime migration of multi-tier applications to AWS multi-region EKS clusters provisioned with Terraform.",
        required_skills=["AWS", "Kubernetes", "Terraform (IaC)", "Prometheus & Grafana", "CI/CD"],
        tech_stack_summary="AWS + Kubernetes + Terraform + Prometheus",
    ),
    7: ProjectRequirement(
        project_id=7,
        project_name="Field Service Mobile App Backend",
        description="Developed offline-first mobile sync backend serving field engineers with GraphQL endpoints and OAuth2 security.",
        required_skills=["React Native", "GraphQL", "Azure Functions", "OAuth2", "Azure SQL"],
        tech_stack_summary="React Native + GraphQL + Azure Functions",
    ),
    8: ProjectRequirement(
        project_id=8,
        project_name="Enterprise Identity & Zero Trust Access Gate",
        description="Centralized company-wide authentication and authorization gateway enforcing strict OAuth2 protocols and JWT verification.",
        required_skills=["OAuth2 / OpenID Connect", "JWT Authentication", "FastAPI", "Redis", "OWASP Security"],
        tech_stack_summary="OAuth2 + JWT + FastAPI + Redis",
    ),
    9: ProjectRequirement(
        project_id=9,
        project_name="Automated End-to-End Testing Suite",
        description="Architected unified cross-browser and regression test automation suite running parallelized runs in CI/CD pipelines.",
        required_skills=["Playwright & Cypress Testing", "PyTest", "GitHub Actions", "Docker"],
        tech_stack_summary="Playwright + Cypress + PyTest + GitHub Actions",
    ),
    10: ProjectRequirement(
        project_id=10,
        project_name="Autonomous RAG Knowledge Assistant",
        description="Implemented enterprise RAG search system indexing codebase repositories and technical handbooks with hybrid vector retrieval.",
        required_skills=["Python", "LangChain", "PyTorch", "Vector Databases", "OpenAI Embeddings", "FastAPI"],
        tech_stack_summary="Python + LangChain + Vector DB + FastAPI",
    ),
    11: ProjectRequirement(
        project_id=11,
        project_name="High-Speed Market Data Ingestion Engine",
        description="Low-latency ingestion daemon ingesting live financial order books with sub-millisecond gRPC processing and Redis buffering.",
        required_skills=["Go (Golang)", "gRPC", "Redis", "Docker", "PostgreSQL"],
        tech_stack_summary="Go + gRPC + Redis + PostgreSQL",
    ),
    12: ProjectRequirement(
        project_id=12,
        project_name="Design System & Accessible Component Library",
        description="Engineered enterprise design system adhering to WCAG 2.1 AA standards, consumed by internal web applications.",
        required_skills=["React", "TypeScript", "Material UI & Styling", "Web Performance Optimization"],
        tech_stack_summary="React + TypeScript + Material UI",
    ),
    13: ProjectRequirement(
        project_id=13,
        project_name="Data Warehouse & Analytics ETL Engine",
        description="Built distributed analytical ETL pipeline aggregating daily product usage metrics into optimized columnar data lakes.",
        required_skills=["Apache Spark", "Python", "PostgreSQL", "AWS Cloud Architecture"],
        tech_stack_summary="Apache Spark + Python + PostgreSQL + AWS",
    ),
    14: ProjectRequirement(
        project_id=14,
        project_name="Observability & Distributed Tracing Stack",
        description="Standardized unified telemetry monitoring with OpenTelemetry, Prometheus metrics alerts, and Grafana interactive squad dashboards.",
        required_skills=["Kubernetes", "Prometheus & Grafana Observability", "Linux", "Docker"],
        tech_stack_summary="Kubernetes + Prometheus + Grafana",
    ),
    15: ProjectRequirement(
        project_id=15,
        project_name="Micro-Frontend Shell & Module Federation",
        description="Designed pluggable micro-frontend shell allowing autonomous squad deployments without coordinated application rollouts.",
        required_skills=["React", "TypeScript", "Vite", "Material UI & Styling"],
        tech_stack_summary="React + TypeScript + Vite + Module Federation",
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
