"""
Employee Upskilling Roadmap Agent
----------------------------------
Single-file, extensible LangChain + Groq agent that takes a skills-gap
analysis result (strengths / gaps / areas of improvement / readiness score)
and generates a concrete, constructive 6-month upskilling roadmap, returned
as a structured JSON payload suitable for rendering on a UI screen.

Extensibility points:
- `ROADMAP_DURATION_MONTHS` controls the timeline length used in the prompt.
- `build_chain()` isolates the LLM/prompt wiring so the model or parser can be swapped independently.
- `run_roadmap_generation()` is the single reusable entry point other modules (e.g. a FastAPI controller) can call.
- Input is the gap-analysis agent's own JSON output, so the two agents compose directly.
"""

import json
import os
from typing import Any

import dotenv
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

dotenv.load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
ROADMAP_DURATION_MONTHS = 6


# --------------------------------------------------------------------------
# Sample data (replace with a real gap-analysis response in production)
# --------------------------------------------------------------------------
SAMPLE_GAP_ANALYSIS: dict[str, Any] = {
    "employee_name": "Anil Kurahatti",
    "experience_years": 4,
    "overall_readiness_score": 55,
    "strengths": [
        {"skill": "C#", "reason": "Strong core language proficiency from .NET Framework experience."},
    ],
    "gaps": [
        {
            "skill": "ASP.NET Core Web API",
            "priority": "High",
            "reason": "No hands-on experience with the modern .NET Core web stack.",
            "recommended_action": "Build a REST API from scratch using ASP.NET Core Web API.",
        },
        {
            "skill": "Docker",
            "priority": "Medium",
            "reason": "No containerization experience.",
            "recommended_action": "Containerize an existing application and deploy it locally.",
        },
    ],
    "areas_of_improvement": [
        {"area": "Cloud deployment", "recommendation": "Get hands-on with Azure App Service deployments."},
    ],
    "summary": "Solid .NET fundamentals; needs modernization toward .NET Core, containers, and cloud.",
}


# --------------------------------------------------------------------------
# Prompt
# --------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert Technical Career Coach and Learning & Development specialist.
You receive a structured skills-gap analysis for an employee (strengths, gaps, areas of
improvement, readiness score) and design a concrete, constructive {months}-month upskilling
roadmap that closes those gaps and grows the employee's career.

Rules:
- Base the roadmap only on the gap analysis data provided in the user message.
- Prioritize High-priority gaps earlier in the timeline, but keep a realistic progression
  (foundational skills before advanced ones).
- Every month must have a distinct, achievable focus - never repeat the same content twice.
- Recommendations must be specific and actionable (named skills, concrete practice tasks,
  concrete resource types), never generic filler like "read more" or "practice more".
- Keep the tone encouraging and constructive - this roadmap should motivate the employee to excel.
- Respond with ONLY valid JSON (no markdown fences, no commentary) matching EXACTLY this structure:

{{
  "employee_name": "string",
  "role": "string",
  "roadmap_duration_months": {months},
  "overall_goal": "string",
  "starting_readiness_score": number,
  "target_readiness_score": number,
  "monthly_plan": [
    {{
      "month": 1,
      "title": "string",
      "focus_skills": ["string"],
      "objectives": ["string"],
      "learning_resources": [
        {{"type": "course|certification|documentation|book|mentorship|workshop", "title": "string", "description": "string"}}
      ],
      "practical_tasks": ["string"],
      "milestone": "string",
      "estimated_weekly_hours": number
    }}
  ],
  "success_metrics": ["string"],
  "summary": "string"
}}

The "monthly_plan" array MUST contain exactly {months} entries, one per month, with "month" values 1 through {months} in order."""


def _format_user_prompt(gap_analysis: dict[str, Any]) -> str:
    """Builds the user-turn content sent to the LLM from the gap-analysis JSON."""
    return (
        f"Design a {ROADMAP_DURATION_MONTHS}-month upskilling roadmap based on the skills-gap "
        "analysis below. Return the JSON described in the system prompt.\n\n"
        f"{json.dumps(gap_analysis, indent=2)}"
    )


def build_chain(model: str = GROQ_MODEL, temperature: float = 0.4):
    """Wires up the LangChain prompt | LLM | parser pipeline. Swap model/parser here."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your .env file before running the agent."
        )

    llm = ChatGroq(api_key=api_key, model=model, temperature=temperature)
    parser = JsonOutputParser()
    # System message is passed as a static BaseMessage (not a templated string) so the
    # literal JSON-example braces in SYSTEM_PROMPT are never re-parsed as template variables.
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_PROMPT.format(months=ROADMAP_DURATION_MONTHS)),
            ("user", "{input}"),
        ]
    )
    return prompt | llm | parser


def run_roadmap_generation(gap_analysis: dict[str, Any], chain=None) -> dict:
    """Single reusable entry point: returns the upskilling roadmap as a JSON-ready dict."""
    chain = chain or build_chain()
    user_input = _format_user_prompt(gap_analysis)
    return chain.invoke({"input": user_input})


if __name__ == "__main__":
    try:
        result = run_roadmap_generation(SAMPLE_GAP_ANALYSIS)
        print("\n--- Upskilling Roadmap JSON (for UI consumption) ---")
        print(json.dumps(result, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
