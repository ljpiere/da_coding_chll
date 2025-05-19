# app/db/models.py
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .session import Base

class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int]          = mapped_column(Integer, primary_key=True)
    department: Mapped[str]  = mapped_column(String, nullable=False)

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job: Mapped[str] = mapped_column(String, nullable=False)

class HiredEmployee(Base):
    __tablename__ = "hired_employees"
    id: Mapped[int]  = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    datetime: Mapped[DateTime(timezone=True)] = mapped_column(DateTime(timezone=True), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)

    department = relationship("Department")
    job        = relationship("Job")
