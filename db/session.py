# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import get_settings

class Base(DeclarativeBase):
    pass

def _engine():
    return create_engine(get_settings().database_uri, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=_engine(), autocommit=False, autoflush=False)
