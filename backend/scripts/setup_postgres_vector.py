"""PostgreSQL and pgvector Setup, Schema Creation, and Raw Data Push Script.

This script:
1. Connects to PostgreSQL using DATABASE_URL from .env (centralized/cloud)
   or individual POSTGRES_* variables (local Docker).
2. Checks if the target database exists and creates it if missing.
3. Activates the `vector` extension (pgvector).
4. Creates all application tables with HNSW vector similarity indexes.
5. Ingests raw seed data for all domain tables.
6. Computes 1536-dim dummy embeddings (no API key required) and stores them.
7. Runs a validation cosine similarity query to confirm pgvector is working.

Usage:
    python scripts/setup_postgres_vector.py              # full run
    python scripts/setup_postgres_vector.py --dry-run    # validate config only, no DB changes
    python scripts/setup_postgres_vector.py --recreate   # DROP and recreate all tables (destructive!)
"""
import argparse
import json
import logging
import math
import os
import random
import sys
from pathlib import Path

# ── Make sure app imports resolve ────────────────────────────────────────────
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import Base
from app.models.db_models import (
    ChatMessageModel,
    DemoItemModel,
    EmployeeFeedbackModel,
    EmployeeModel,
    EmployeeProjectModel,
    EmployeeSkillModel,
    VectorDocumentModel,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("setup_postgres_vector")

EMBEDDING_DIMENSION = 1536

# ─────────────────────────────────────────────────────────────────────────────
# RAW SEED DATA
# This is the raw data that gets embedded and stored in PostgreSQL.
# Embeddings represent the semantic meaning of the text fields below.
# ─────────────────────────────────────────────────────────────────────────────

RAW_EMPLOYEES = [
    {
        "name": "Jane Doe",
        "email": "jane.doe@squad4.dev",
        "title": "Senior Backend Engineer",
        "department": "Core Platform",
        "total_experience_years": 6.0,
        "bio": "Specializes in high-throughput FastAPI microservices and async Python APIs.",
    },
    {
        "name": "John Smith",
        "email": "john.smith@squad4.dev",
        "title": "Frontend Engineer",
        "department": "UX Platform",
        "total_experience_years": 4.0,
        "bio": "Builds React component libraries and performance-optimized UIs.",
    },
    {
        "name": "Alex Lee",
        "email": "alex.lee@squad4.dev",
        "title": "Full-Stack Engineer",
        "department": "Core Platform",
        "total_experience_years": 5.0,
        "bio": "Experienced in both FastAPI backend and React frontend with a DevOps mindset.",
    },
    {
        "name": "Priya Sharma",
        "email": "priya.sharma@squad4.dev",
        "title": "Data & AI Engineer",
        "department": "AI Platform",
        "total_experience_years": 7.0,
        "bio": "Expert in PostgreSQL, pgvector, and ML pipeline architecture.",
    },
    {
        "name": "Carlos Rodriguez",
        "email": "carlos.rodriguez@squad4.dev",
        "title": "DevOps Engineer",
        "department": "Infrastructure",
        "total_experience_years": 5.5,
        "bio": "Manages Docker, Kubernetes clusters, and CI/CD pipelines at scale.",
    },
]

# employee_id is assigned by insertion order (1-indexed matching RAW_EMPLOYEES)
RAW_EMPLOYEE_SKILLS = [
    {
        "employee_id": 1, "employee_name": "Jane Doe",
        "skill_name": "Python & FastAPI", "proficiency_level": "Expert", "years_of_experience": 5.0,
    },
    {
        "employee_id": 1, "employee_name": "Jane Doe",
        "skill_name": "PostgreSQL", "proficiency_level": "Advanced", "years_of_experience": 3.5,
    },
    {
        "employee_id": 2, "employee_name": "John Smith",
        "skill_name": "React & Frontend Architecture", "proficiency_level": "Intermediate", "years_of_experience": 3.0,
    },
    {
        "employee_id": 2, "employee_name": "John Smith",
        "skill_name": "TypeScript", "proficiency_level": "Advanced", "years_of_experience": 2.5,
    },
    {
        "employee_id": 3, "employee_name": "Alex Lee",
        "skill_name": "FastAPI & Microservices", "proficiency_level": "Advanced", "years_of_experience": 4.0,
    },
    {
        "employee_id": 4, "employee_name": "Priya Sharma",
        "skill_name": "PostgreSQL & pgvector Search", "proficiency_level": "Expert", "years_of_experience": 4.0,
    },
    {
        "employee_id": 4, "employee_name": "Priya Sharma",
        "skill_name": "Machine Learning & Embeddings", "proficiency_level": "Advanced", "years_of_experience": 3.0,
    },
    {
        "employee_id": 5, "employee_name": "Carlos Rodriguez",
        "skill_name": "Docker, Kubernetes & CI/CD", "proficiency_level": "Intermediate", "years_of_experience": 3.5,
    },
]

RAW_EMPLOYEE_PROJECTS = [
    {
        "employee_id": 1, "employee_name": "Jane Doe",
        "project_name": "Engineer Pulse API", "role": "Lead Backend Architect",
        "technologies": "FastAPI, PostgreSQL, pgvector, Docker",
        "description": "Designed and built the entire FastAPI backend with layered architecture and AI-powered search.",
        "duration_months": 6,
    },
    {
        "employee_id": 2, "employee_name": "John Smith",
        "project_name": "Engineer Pulse Frontend", "role": "UI Developer",
        "technologies": "React, Vite, Material UI, Recharts",
        "description": "Built the React frontend including dashboard charts, feedback forms, and chatbot interface.",
        "duration_months": 6,
    },
    {
        "employee_id": 3, "employee_name": "Alex Lee",
        "project_name": "Chatbot Integration", "role": "Full-Stack Engineer",
        "technologies": "FastAPI, React, OpenAI API",
        "description": "Integrated Azure OpenAI chatbot backend with streaming support and session-based chat history.",
        "duration_months": 3,
    },
    {
        "employee_id": 4, "employee_name": "Priya Sharma",
        "project_name": "pgvector Semantic Search Engine", "role": "AI/ML Engineer",
        "technologies": "PostgreSQL, pgvector, Python, OpenAI Embeddings",
        "description": "Designed the vector embedding pipeline and HNSW index strategy for sub-100ms cosine search.",
        "duration_months": 4,
    },
    {
        "employee_id": 5, "employee_name": "Carlos Rodriguez",
        "project_name": "DevOps Pipeline & Docker Setup", "role": "Infrastructure Lead",
        "technologies": "Docker Compose, GitHub Actions, Azure DevOps",
        "description": "Set up Docker Compose for local development and CI/CD pipelines for automated testing and deployment.",
        "duration_months": 2,
    },
]

RAW_EMPLOYEE_FEEDBACK = [
    {
        "employee_id": 1, "employee_name": "Jane Doe",
        "reviewer_name": "Priya Sharma",
        "feedback_text": "Great collaboration on the sprint. Delivered async endpoints on schedule with excellent test coverage.",
        "rating": 5,
    },
    {
        "employee_id": 2, "employee_name": "John Smith",
        "reviewer_name": "Alex Lee",
        "feedback_text": "Needs to improve code review turnaround times and increase unit test coverage.",
        "rating": 3,
    },
    {
        "employee_id": 3, "employee_name": "Alex Lee",
        "reviewer_name": "Jane Doe",
        "feedback_text": "Consistently delivers high quality work and actively assists junior teammates.",
        "rating": 4,
    },
    {
        "employee_id": 4, "employee_name": "Priya Sharma",
        "reviewer_name": "Carlos Rodriguez",
        "feedback_text": "Outstanding problem-solving skills, deep architectural mentorship, and database optimization insights.",
        "rating": 5,
    },
    {
        "employee_id": 5, "employee_name": "Carlos Rodriguez",
        "reviewer_name": "John Smith",
        "feedback_text": "Active participant in sprint retrospectives, very supportive teammate, and reliable on delivery.",
        "rating": 4,
    },
]

RAW_CHAT_MESSAGES = [
    {"session_id": "session-001", "sender": "user", "message": "Hi, what can you help me with?"},
    {"session_id": "session-001", "sender": "bot",  "message": "I can help you analyze employee feedback and query squad skills via AI."},
    {"session_id": "session-002", "sender": "user", "message": "Who has the most experience with PostgreSQL?"},
    {"session_id": "session-002", "sender": "bot",  "message": "Priya Sharma has Expert-level PostgreSQL & pgvector experience with 4 years in the domain."},
]

RAW_VECTOR_DOCUMENTS = [
    {
        "title": "Engineer Pulse Project Charter",
        "category": "project_info",
        "content": (
            "Engineer Pulse is an APEX Batch 4 platform designed to provide real-time insights "
            "into squad velocity, engineering skills, and employee sentiment through interactive "
            "dashboards and AI-assisted vector search."
        ),
        "metadata_json": json.dumps({"batch": "Batch 4", "squad": "Squad 4"}),
    },
    {
        "title": "pgvector Architecture Guide",
        "category": "technical_guide",
        "content": (
            "pgvector is an open-source vector similarity search extension for PostgreSQL. "
            "It enables storing high-dimensional embeddings alongside relational data, "
            "supporting exact and approximate nearest-neighbor search with HNSW and IVFFlat indexes."
        ),
        "metadata_json": json.dumps({"component": "database", "extension": "pgvector"}),
    },
    {
        "title": "FastAPI Layered Architecture",
        "category": "technical_guide",
        "content": (
            "The backend follows a three-layer architecture: controllers handle HTTP "
            "request/response, business services contain domain logic, and repositories "
            "manage database access via SQLAlchemy ORM."
        ),
        "metadata_json": json.dumps({"component": "backend", "pattern": "layered-architecture"}),
    },
]

RAW_DEMO_ITEMS = [
    {"name": "Sample Item One", "description": "Seeded demo item for testing GET/PUT/DELETE."},
    {"name": "Sample Item Two", "description": "Second seeded demo item for CRUD validation."},
]


# ─────────────────────────────────────────────────────────────────────────────
# EMBEDDING GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def _generate_dummy_embedding(text: str, dimension: int = EMBEDDING_DIMENSION) -> list[float]:
    """
    Generate a reproducible unit-normalized pseudo-embedding from text.

    This is used when no OpenAI API key is configured.
    It creates a deterministic vector seeded by the text content so that
    similar texts produce different vectors — good enough for schema validation
    and pgvector cosine query testing without calling any external API.

    Replace this with real OpenAI embeddings for production.
    """
    rng = random.Random(hash(text) % (2**31))
    vec = [rng.gauss(0, 1) for _ in range(dimension)]
    # Normalize to unit length for cosine similarity
    magnitude = math.sqrt(sum(x * x for x in vec))
    return [x / magnitude for x in vec]


def _try_openai_embedding(text: str, settings) -> list[float] | None:
    """Attempt to generate a real OpenAI embedding. Returns None if unavailable."""
    if not settings.openai_api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(model="text-embedding-3-small", input=text)
        return response.data[0].embedding
    except Exception as exc:
        logger.warning(f"OpenAI embedding failed, falling back to dummy: {exc}")
        return None


def get_embedding(text: str, settings) -> list[float]:
    """Get embedding: real OpenAI if API key present, otherwise deterministic dummy."""
    real = _try_openai_embedding(text, settings)
    if real:
        return real
    return _generate_dummy_embedding(text)


# ─────────────────────────────────────────────────────────────────────────────
# DATABASE SETUP STEPS
# ─────────────────────────────────────────────────────────────────────────────

def ensure_database_exists(db_url: str) -> None:
    """Connect to the default 'postgres' system DB and create target DB if it doesn't exist."""
    url = make_url(db_url)
    target_db = url.database
    if not target_db:
        return

    admin_url = url.set(database="postgres")
    try:
        admin_engine = create_engine(str(admin_url), isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": target_db},
            ).scalar()
            if not exists:
                logger.info(f"Database '{target_db}' not found. Creating it...")
                conn.execute(text(f'CREATE DATABASE "{target_db}"'))
                logger.info(f"✅ Database '{target_db}' created.")
            else:
                logger.info(f"✅ Database '{target_db}' already exists.")
        admin_engine.dispose()
    except Exception as exc:
        logger.warning(
            f"Could not auto-create database (may already exist or insufficient permissions): {exc}"
        )


def enable_pgvector(engine) -> bool:
    """Run CREATE EXTENSION IF NOT EXISTS vector and verify it is active."""
    logger.info("Enabling pgvector extension...")
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        result = conn.execute(
            text("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';")
        ).fetchone()
    if result:
        logger.info(f"✅ pgvector extension ACTIVE — version {result[1]}")
        return True
    logger.error("❌ pgvector extension not found after CREATE EXTENSION. Is pgvector installed?")
    return False


def create_tables_and_indexes(engine, force_recreate: bool = False) -> None:
    """Create all ORM tables and HNSW vector indexes."""
    if force_recreate:
        logger.info("⚠️  Dropping all existing tables (--recreate flag)...")
        Base.metadata.drop_all(bind=engine)

    logger.info("Creating application tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ All tables created/verified.")

    # HNSW vector indexes for fast approximate cosine similarity search
    hnsw_indexes = [
        (
            "idx_employee_skills_embedding_hnsw", "employee_skills",
            "CREATE INDEX IF NOT EXISTS idx_employee_skills_embedding_hnsw "
            "ON employee_skills USING hnsw (embedding vector_cosine_ops);",
        ),
        (
            "idx_employee_projects_embedding_hnsw", "employee_projects",
            "CREATE INDEX IF NOT EXISTS idx_employee_projects_embedding_hnsw "
            "ON employee_projects USING hnsw (embedding vector_cosine_ops);",
        ),
        (
            "idx_employee_feedback_embedding_hnsw", "employee_feedback",
            "CREATE INDEX IF NOT EXISTS idx_employee_feedback_embedding_hnsw "
            "ON employee_feedback USING hnsw (embedding vector_cosine_ops);",
        ),
        (
            "idx_vector_docs_embedding_hnsw", "vector_documents",
            "CREATE INDEX IF NOT EXISTS idx_vector_docs_embedding_hnsw "
            "ON vector_documents USING hnsw (embedding vector_cosine_ops);",
        ),
    ]

    with engine.begin() as conn:
        for idx_name, tbl_name, sql in hnsw_indexes:
            try:
                conn.execute(text(sql))
                logger.info(f"  ✅ HNSW index '{idx_name}' on '{tbl_name}'")
            except Exception as exc:
                logger.warning(f"  ⚠️  Could not create {idx_name}: {exc}")


def push_seed_data(engine, settings) -> dict[str, int]:
    """Insert raw seed data and generate vector embeddings for each text field."""
    stats: dict[str, int] = {}

    with Session(engine) as session:

        # 1. Employees (master profile — no embedding)
        if session.query(EmployeeModel).count() == 0:
            logger.info("Inserting employees...")
            for row in RAW_EMPLOYEES:
                session.add(EmployeeModel(**row))
            session.flush()
            stats["employees"] = len(RAW_EMPLOYEES)
            logger.info(f"  ✅ {len(RAW_EMPLOYEES)} employees inserted")
        else:
            logger.info("  ⏭️  Employees table already has data, skipping.")
            stats["employees"] = 0

        # 2. Employee Skills (embedding: skill_name + proficiency)
        if session.query(EmployeeSkillModel).count() == 0:
            logger.info("Inserting employee skills + embeddings...")
            for row in RAW_EMPLOYEE_SKILLS:
                embed_text = f"{row['employee_name']} has {row['proficiency_level']} proficiency in {row['skill_name']} with {row['years_of_experience']} years experience."
                embedding = get_embedding(embed_text, settings)
                session.add(EmployeeSkillModel(**row, embedding=embedding))
            session.flush()
            stats["skills"] = len(RAW_EMPLOYEE_SKILLS)
            logger.info(f"  ✅ {len(RAW_EMPLOYEE_SKILLS)} skills inserted with embeddings")
        else:
            logger.info("  ⏭️  Skills table already has data, skipping.")
            stats["skills"] = 0

        # 3. Employee Projects (embedding: role + description + technologies)
        if session.query(EmployeeProjectModel).count() == 0:
            logger.info("Inserting employee projects + embeddings...")
            for row in RAW_EMPLOYEE_PROJECTS:
                embed_text = f"{row['employee_name']} worked as {row['role']} on {row['project_name']} using {row['technologies']}. {row['description']}"
                embedding = get_embedding(embed_text, settings)
                session.add(EmployeeProjectModel(**row, embedding=embedding))
            session.flush()
            stats["projects"] = len(RAW_EMPLOYEE_PROJECTS)
            logger.info(f"  ✅ {len(RAW_EMPLOYEE_PROJECTS)} projects inserted with embeddings")
        else:
            logger.info("  ⏭️  Projects table already has data, skipping.")
            stats["projects"] = 0

        # 4. Employee Feedback (embedding: feedback_text)
        if session.query(EmployeeFeedbackModel).count() == 0:
            logger.info("Inserting employee feedback + embeddings...")
            for row in RAW_EMPLOYEE_FEEDBACK:
                embed_text = f"{row['reviewer_name']} reviewed {row['employee_name']}: {row['feedback_text']} (Rating: {row['rating']}/5)"
                embedding = get_embedding(embed_text, settings)
                session.add(EmployeeFeedbackModel(**row, embedding=embedding))
            session.flush()
            stats["feedback"] = len(RAW_EMPLOYEE_FEEDBACK)
            logger.info(f"  ✅ {len(RAW_EMPLOYEE_FEEDBACK)} feedback entries inserted with embeddings")
        else:
            logger.info("  ⏭️  Feedback table already has data, skipping.")
            stats["feedback"] = 0

        # 5. Chat Messages (no embedding)
        if session.query(ChatMessageModel).count() == 0:
            logger.info("Inserting chat messages...")
            for row in RAW_CHAT_MESSAGES:
                session.add(ChatMessageModel(**row))
            session.flush()
            stats["chat"] = len(RAW_CHAT_MESSAGES)
            logger.info(f"  ✅ {len(RAW_CHAT_MESSAGES)} chat messages inserted")
        else:
            logger.info("  ⏭️  Chat messages table already has data, skipping.")
            stats["chat"] = 0

        # 6. Vector Documents (embedding: title + content)
        if session.query(VectorDocumentModel).count() == 0:
            logger.info("Inserting vector documents (RAG KB) + embeddings...")
            for row in RAW_VECTOR_DOCUMENTS:
                embed_text = f"{row['title']}: {row['content']}"
                embedding = get_embedding(embed_text, settings)
                session.add(VectorDocumentModel(**row, embedding=embedding))
            session.flush()
            stats["docs"] = len(RAW_VECTOR_DOCUMENTS)
            logger.info(f"  ✅ {len(RAW_VECTOR_DOCUMENTS)} knowledge documents inserted with embeddings")
        else:
            logger.info("  ⏭️  Vector documents table already has data, skipping.")
            stats["docs"] = 0

        # 7. Demo Items (no embedding)
        if session.query(DemoItemModel).count() == 0:
            for row in RAW_DEMO_ITEMS:
                session.add(DemoItemModel(**row))
            stats["demo"] = len(RAW_DEMO_ITEMS)
        else:
            stats["demo"] = 0

        session.commit()

    return stats


def validate_vector_search(engine, settings) -> None:
    """Run a sample cosine similarity search to confirm pgvector is operational."""
    logger.info("\n── pgvector Validation: Cosine Similarity Search ──")
    query_text = "expert in Python and backend API development"
    query_vec = get_embedding(query_text, settings)
    query_vec_str = f"[{','.join(str(x) for x in query_vec)}]"

    with engine.connect() as conn:
        results = conn.execute(
            text(
                "SELECT employee_name, skill_name, proficiency_level, "
                "embedding <=> CAST(:qv AS vector) AS distance "
                "FROM employee_skills "
                "ORDER BY distance ASC LIMIT 3;"
            ),
            {"qv": query_vec_str},
        ).fetchall()

    if results:
        logger.info(f"  Query: '{query_text}'")
        for i, r in enumerate(results, 1):
            similarity = round(1.0 - r[3], 4) if r[3] is not None else 0.0
            logger.info(f"  #{i} {r[0]} | {r[1]} ({r[2]}) | similarity={similarity:.4f}")
        logger.info("  ✅ pgvector cosine similarity search is working correctly!")
    else:
        logger.warning("  ⚠️  No results returned from vector search — check that embeddings were inserted.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Engineer Pulse PostgreSQL + pgvector setup script")
    parser.add_argument("--dry-run",  action="store_true", help="Validate config only, no DB writes")
    parser.add_argument("--recreate", action="store_true", help="Drop and recreate all tables (destructive!)")
    args = parser.parse_args()

    settings = get_settings()
    db_url = settings.effective_database_url

    logger.info("=" * 65)
    logger.info("  Engineer Pulse — PostgreSQL + pgvector Setup")
    logger.info("=" * 65)
    logger.info(f"  Connection : {db_url.split('@')[-1] if '@' in db_url else db_url}")
    logger.info(f"  Embedding  : {'Real (OpenAI)' if settings.openai_api_key else 'Dummy (deterministic, no API key)'}")
    logger.info(f"  Mode       : {'DRY RUN — no changes will be written' if args.dry_run else 'LIVE'}")
    logger.info("=" * 65)

    if args.dry_run:
        logger.info("✅ Dry-run complete. Config looks valid.")
        return

    # Step 1: Ensure target database exists
    ensure_database_exists(db_url)

    # Step 2: Connect engine
    engine = create_engine(db_url, pool_pre_ping=True)

    # Step 3: Enable pgvector
    if not enable_pgvector(engine):
        logger.error("Aborting: pgvector extension could not be enabled.")
        sys.exit(1)

    # Step 4: Create tables and HNSW indexes
    create_tables_and_indexes(engine, force_recreate=args.recreate)

    # Step 5: Insert seed data + embeddings
    logger.info("\nInserting seed data and generating embeddings...")
    stats = push_seed_data(engine, settings)
    logger.info(f"\n  Seed summary: {stats}")

    # Step 6: Validate with a real cosine similarity query
    validate_vector_search(engine, settings)

    engine.dispose()
    logger.info("\n✅ Setup complete! Database is ready.")
    logger.info(
        "   Share this DATABASE_URL with your team (keep it out of Git!):\n"
        f"   DATABASE_URL={db_url}"
    )


if __name__ == "__main__":
    main()
