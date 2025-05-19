# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import get_settings

class Base(DeclarativeBase):
    pass

def _engine():
    # casteo de la uri de la db a string
    return create_engine(
        str(get_settings().database_uri),   #obtener config prov de env
        pool_pre_ping=True,
        future=True,
    )

SessionLocal = sessionmaker(bind=_engine(), autocommit=False, autoflush=False)
