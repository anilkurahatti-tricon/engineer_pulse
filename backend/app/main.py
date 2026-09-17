"""FastAPI application entrypoint.

Wires up the layered architecture: controllers (API) -> business (services)
-> dataservice (repositories), plus the AI integration layer used by the
chatbot controller. Swagger/OpenAPI docs are enabled by default at /docs.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    chatbot_controller,
    demo_controller,
    employee_feedback_controller,
    employee_skills_controller,
    welcome_controller,
)
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Engineer Pulse API - employee feedback, employee skills, and an "
        "AI-powered chatbot, backed by a layered controller/business/dataservice "
        "architecture. No authentication is enabled at this stage."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS is wide open since there is no authentication yet and the React app
# runs on a different origin/port during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_allow_origins] if settings.cors_allow_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(welcome_controller.router)
app.include_router(demo_controller.router)
app.include_router(employee_feedback_controller.router)
app.include_router(employee_skills_controller.router)
app.include_router(chatbot_controller.router)


@app.get("/", tags=["Health"], summary="Health check")
def read_root() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}
