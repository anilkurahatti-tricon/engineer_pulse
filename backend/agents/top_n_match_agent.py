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
from typing import List

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
# Prompt
# --------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert Technical Career Coach and Talent-Matching Analyst.
You compare ONE target project's required skills against a pool of employees and score
EVERY employee's readiness for that project, using the same methodology a skills-gap
analysis would use.

Rules:
- Base your analysis only on the project and employee data provided in the user message.
- You MUST score every single employee in the input list - never omit one.
- "overall_readiness_score" is an integer 0-100 estimating how ready the employee is for
  this project today, considering skill coverage, proficiency depth, and relevant experience.
- "matched_skills" are required project skills the employee already has.
- "missing_skills" are required project skills the employee does NOT currently have.
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
    """Builds the user-turn content sent to the LLM from structured data."""
    from dataclasses import asdict

    payload = {
        "project": asdict(project),
        "employees": [asdict(e) for e in employees],
    }
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

    # Map scored candidates back to employee_id by name so API consumers can link to a profile.
    employee_id_by_name = {e.name: e.employee_id for e in employees}
    candidates = result.get("candidates", [])
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
