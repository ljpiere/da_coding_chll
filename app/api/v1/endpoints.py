# app/api/v1/endpoints.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from app.db.session import SessionLocal
from app.db import models as m
from pathlib import Path
from typing import Annotated, List

router = APIRouter()

def get_db() -> Session:      # dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# carga CSV a DB
TARGET_MAP = {
    "departments": m.Department,
    "jobs": m.Job,
    "hired_employees": m.HiredEmployee,
}

COLS = {
    "departments": ["id", "department"],
    "jobs": ["id", "job"],
    "hired_employees": ["id", "name", "datetime", "department_id", "job_id"],
}

# @router.post("/upload_csv")
# async def upload_csv(
#     target: str,
#     file: Annotated[UploadFile, File(... )],
#     db: Session = Depends(get_db),
# ):
#     if target not in TARGET_MAP:
#         raise HTTPException(400, "target inválido")
#     df = pd.read_csv(file.file, header=None, names=COLS[target])
#     df.to_sql(TARGET_MAP[target].__tablename__, db.bind, if_exists="append", index=False)
#     return {"rows_inserted": len(df)}

@router.post("/upload_csv")
async def upload_csv(target: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if target not in TARGET_MAP:
        raise HTTPException(400, "target inválido")

    # lee SIEMPRE sin cabecera y asigna nombres
    df = pd.read_csv(file.file, header=None, names=COLS[target])

    df.to_sql(TARGET_MAP[target].__tablename__, db.bind,
              if_exists="append", index=False)
    return {"rows_inserted": len(df)}
# Inserción batch 
from pydantic import BaseModel, field_validator
from datetime import datetime

class EmployeeIn(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

    @field_validator("datetime")
    def zulu(cls, v):      # normalizar formato ISO-Z
        return v.replace(tzinfo=None)

@router.post("/employees/batch", status_code=201)
async def batch_employees(
    employees: List[EmployeeIn],
    db: Session = Depends(get_db),
):
    if not 1 <= len(employees) <= 1000:
        raise HTTPException(400, "Batch fuera de rango (1-1000)")
    db.bulk_insert_mappings(m.HiredEmployee, [e.model_dump() for e in employees])
    db.commit()
    return {"inserted": len(employees)}

# métricas 2021
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent / "queries"
SQL = (BASE_DIR / "metrics.sql").read_text()

@router.get("/metrics/hires-2021")
def hires_2021(db: Session = Depends(get_db)):
    query = SQL.split(";")[0]   # primero de metrics.sql
    return db.execute(text(query)).mappings().all()

@router.get("/metrics/above-average-2021")
def above_avg_2021(db: Session = Depends(get_db)):
    query = SQL.split(";")[1]   # segundo de metrics.sql
    return db.execute(text(query)).mappings().all()
