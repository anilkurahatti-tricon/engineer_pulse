"""SQLAlchemy ORM models mapped to PostgreSQL tables, including pgvector columns."""
from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

EMBEDDING_DIMENSION = 1536


class EmployeeModel(Base):
    """SQLAlchemy model for the central employee profile table."""

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)           # e.g. Senior Backend Engineer
    department: Mapped[str] = mapped_column(String(100), nullable=False)      # e.g. Core Platform
    total_experience_years: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False, default=0.0)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class EmployeeSkillModel(Base):
    """SQLAlchemy model for employee skills with pgvector embedding."""

    __tablename__ = "employee_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    proficiency_level: Mapped[str] = mapped_column(String(50), nullable=False)  # Beginner|Intermediate|Advanced|Expert
    years_of_experience: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    # 1536-dimensional vector embedding for talent search / skill matching
    embedding = mapped_column(Vector(EMBEDDING_DIMENSION), nullable=True)


class EmployeeProjectModel(Base):
    """SQLAlchemy model for projects employees have worked on."""

    __tablename__ = "employee_projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)            # e.g. Lead Backend Architect
    technologies: Mapped[str] = mapped_column(String(255), nullable=False)   # e.g. FastAPI, PostgreSQL, Docker
    description: Mapped[str] = mapped_column(Text, nullable=False)
    duration_months: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    # 1536-dimensional vector for semantic project/experience matching
    embedding = mapped_column(Vector(EMBEDDING_DIMENSION), nullable=True)


class EmployeeFeedbackModel(Base):
    """SQLAlchemy model for employee feedback with pgvector embedding."""

    __tablename__ = "employee_feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    reviewer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    feedback_text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)              # 1 to 5
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    # 1536-dimensional vector embedding for semantic feedback/sentiment search
    embedding = mapped_column(Vector(EMBEDDING_DIMENSION), nullable=True)


class ChatMessageModel(Base):
    """SQLAlchemy model for chat history messages."""

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    sender: Mapped[str] = mapped_column(String(20), nullable=False)           # "user" | "bot"
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class VectorDocumentModel(Base):
    """SQLAlchemy model for general documentation / knowledge base embeddings (RAG)."""

    __tablename__ = "vector_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="general", index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    embedding = mapped_column(Vector(EMBEDDING_DIMENSION), nullable=False)


class DemoItemModel(Base):
    """SQLAlchemy model for demo sandbox items."""

    __tablename__ = "demo_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
