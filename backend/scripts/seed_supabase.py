"""Direct database seeder for Supabase PostgreSQL + pgvector.

Usage:
    cd backend
    python scripts/seed_supabase.py

This script:
1. Connects to Supabase via DATABASE_URL in .env.
2. Idempotently inserts 15 employees, 40 skills, 20 projects, and 15 feedbacks.
3. Automatically computes vector embeddings (OpenAI if key is set, else deterministic).
4. Skips already-existing records so you can run it safely at any time.
"""
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.models.db_models import (
    EmployeeModel,
    EmployeeSkillModel,
    EmployeeProjectModel,
    EmployeeFeedbackModel,
)
from scripts.setup_postgres_vector import push_seed_data


def main():
    print("=" * 65)
    print("  Engineer Pulse — Supabase Data Seeder")
    print("=" * 65)

    settings = get_settings()
    db_url = settings.effective_database_url

    masked_url = db_url.split("@")[-1] if "@" in db_url else db_url
    print(f"📡 Connecting to database: {masked_url}")

    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        # Test connection
        with engine.connect() as conn:
            print(" Connected to Supabase successfully!")
    except Exception as exc:
        print(f"❌ Failed to connect to database: {exc}")
        sys.exit(1)

    print("\n🌱 Seeding missing employees, projects, skills, and feedback...")
    stats = push_seed_data(engine, settings)

    print("\n Seed results for this run:")
    for table_name, count in stats.items():
        print(f"  • {table_name:12}: {count} new record(s) inserted")

    with Session(engine) as session:
        emp_count = session.query(EmployeeModel).count()
        proj_count = session.query(EmployeeProjectModel).count()
        skill_count = session.query(EmployeeSkillModel).count()
        fb_count = session.query(EmployeeFeedbackModel).count()

        print("\n📊 Current Database Totals:")
        print(f"  • Total Employees        : {emp_count}")
        print(f"  • Total Projects         : {proj_count}")
        print(f"  • Total Employee Skills  : {skill_count}")
        print(f"  • Total Feedbacks        : {fb_count}")

    engine.dispose()
    print("\n Database is ready and up to date!\n")


if __name__ == "__main__":
    main()
