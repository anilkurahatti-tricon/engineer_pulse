"""
Employee Tech-Skill Gap Analysis Agent
---------------------------------------
Single-file, extensible LangChain + Groq agent that compares an employee's
current tech skills against the requirements of a set of sample projects,
and returns a structured JSON payload (strengths / gaps / areas of
improvement / readiness score) suitable for rendering on a UI screen.

Extensibility points:
- `Employee` / `ProjectRequirement` dataclasses can be extended with new fields.
- `SAMPLE_PROJECTS` is just a list -> add/remove/load-from-DB without touching the agent logic.
- `build_chain()` isolates the LLM/prompt wiring so the model or parser can be swapped independently.
- `run_gap_analysis()` is the single reusable entry point other modules (e.g. a FastAPI controller) can call.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional

import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

dotenv.load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


# --------------------------------------------------------------------------
# Domain models (extensible: add fields like certifications, domain, etc.)
# --------------------------------------------------------------------------
@dataclass
class Employee:
    name: str
    experience_years: float
    current_skills: List[str]
    role: str = "Software Engineer"


@dataclass
class ProjectRequirement:
    project_name: str
    description: str
    required_skills: List[str]
    tech_stack_summary: Optional[str] = field(default=None)


# --------------------------------------------------------------------------
# Sample data (replace with real data from the DB / API in production)
# --------------------------------------------------------------------------
SAMPLE_EMPLOYEE = Employee(
    name="Rohan Mehta",
    experience_years=4,
    current_skills=[".NET Framework", "ASP.NET MVC", "C#"],
    role="Software Engineer",
)

SAMPLE_PROJECTS: List[ProjectRequirement] = [
    ProjectRequirement(
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
    ProjectRequirement(
        project_name="Inventory Management Microservices Platform",
        description=(
            "A distributed inventory system built as independent .NET microservices "
            "communicating over REST and messaging queues, deployed on Kubernetes."
        ),
        required_skills=[
            ".NET Microservices", "REST API design", "RabbitMQ", "Docker",
            "Kubernetes", "gRPC", "PostgreSQL", "React", "GitHub Actions CI/CD",
            "Redis caching",
        ],
        tech_stack_summary=".NET Microservices + Docker/Kubernetes + React",
    ),
    ProjectRequirement(
        project_name="Field Service Mobile Backend",
        description=(
            "Serverless backend exposing REST and GraphQL endpoints for a "
            "React Native field-service mobile app, secured with OAuth2."
        ),
        required_skills=[
            "ASP.NET Core Web API", "REST API design", "GraphQL", "Azure Functions",
            "Azure SQL", "OAuth2 / OpenID Connect", "Terraform (IaC)", "NUnit",
            "React Native integration",
        ],
        tech_stack_summary=".NET Serverless + GraphQL + Azure",
    ),
]


SYSTEM_PROMPT = """You are an expert Technical Career Coach and Skills Gap Analyst.
You compare an employee's current technical skills against the combined skill
requirements of a set of target projects, and produce an honest, constructive
gap analysis.

Rules:
- Base your analysis only on the employee and project data provided in the user message.
- "strengths" are skills the employee already has that are relevant to the projects.
- "gaps" are required project skills the employee does NOT currently have, ranked by priority.
- "areas_of_improvement" are broader recommendations (e.g. learning paths, certifications, hands-on practice) to close the gaps.
- "overall_readiness_score" is an integer 0-100 estimating how ready the employee is for these projects today.
- Be specific: reference concrete skill names from the project requirements, not generic advice.
- Respond with ONLY valid JSON (no markdown fences, no commentary) matching EXACTLY this structure:

{{
  "employee_name": "string",
  "experience_years": number,
  "overall_readiness_score": number,
  "strengths": [
    {{"skill": "string", "reason": "string"}}
  ],
  "gaps": [
    {{"skill": "string", "priority": "High|Medium|Low", "reason": "string", "recommended_action": "string"}}
  ],
  "areas_of_improvement": [
    {{"area": "string", "recommendation": "string"}}
  ],
  "summary": "string"
}}"""


def _format_user_prompt(employee: Employee, projects: List[ProjectRequirement]) -> str:
    """Builds the user-turn content sent to the LLM from structured data."""
    payload = {
        "employee": asdict(employee),
        "target_projects": [asdict(p) for p in projects],
    }
    return (
        "Analyze the gap between the employee's current skills and the skills "
        "required across all target projects below. Return the JSON described "
        "in the system prompt.\n\n"
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


def run_gap_analysis(
    employee: Employee,
    projects: List[ProjectRequirement],
    chain=None,
) -> dict:
    """Single reusable entry point: returns the gap analysis as a JSON-ready dict."""
    chain = chain or build_chain()
    user_input = _format_user_prompt(employee, projects)
    return chain.invoke({"input": user_input})


def _prompt_for_employee_override(default: Employee) -> Employee:
    """Optional interactive override of the sample employee (press Enter to accept defaults)."""
    print(f"\nUsing sample employee. Press Enter to accept the default, or type a new value.")
    name = input(f"Name [{default.name}]: ").strip() or default.name
    exp_raw = input(f"Experience years [{default.experience_years}]: ").strip()
    experience_years = float(exp_raw) if exp_raw else default.experience_years
    skills_raw = input(f"Current skills, comma-separated [{', '.join(default.current_skills)}]: ").strip()
    current_skills = [s.strip() for s in skills_raw.split(",")] if skills_raw else default.current_skills
    return Employee(name=name, experience_years=experience_years, current_skills=current_skills, role=default.role)


if __name__ == "__main__":
    try:
        employee = _prompt_for_employee_override(SAMPLE_EMPLOYEE)
        result = run_gap_analysis(employee, SAMPLE_PROJECTS)
        print("\n--- Gap Analysis JSON (for UI consumption) ---")
        print(json.dumps(result, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
