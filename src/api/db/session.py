import sqlmodel
from sqlmodel import SQLModel, Session, create_engine
import timescaledb
from sqlalchemy.exc import OperationalError

from .config import DATABASE_URL, DB_TIMEZONE
from fastapi import HTTPException

_engine = None
_is_postgres = False


def has_database() -> bool:
    """Always returns True - we support both PostgreSQL and SQLite fallback"""
    return True


def is_postgres() -> bool:
    """Check if using PostgreSQL with TimescaleDB"""
    get_engine()  # Ensure engine is initialized
    return _is_postgres


def get_engine():
    global _engine, _is_postgres
    if _engine is None:
        if DATABASE_URL and DATABASE_URL != 'sqlite:///test.db':
            # Use TimescaleDB for PostgreSQL
            try:
                _engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)
                _is_postgres = True
                print("Using PostgreSQL with TimescaleDB")
            except Exception as e:
                print(f"Failed to connect to PostgreSQL: {e}. Falling back to SQLite")
                _engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})
                _is_postgres = False
        else:
            # Use SQLite fallback
            _engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})
            _is_postgres = False
            print("Using SQLite database")
    return _engine


def init_db():
    """Initialize the database (create tables)"""
    engine = get_engine()
    print("Creating database tables...")
    try:
        SQLModel.metadata.create_all(engine)
        if _is_postgres:
            print("Creating hypertables...")
            timescaledb.metadata.create_all(engine)
        print("Database initialized successfully")
    except Exception as exc:
        print(f"Warning: Could not fully initialize database: {exc}")
        # Don't raise - allow fallback to work


def get_session():
    """Get a database session"""
    try:
        with Session(get_engine()) as session:
            yield session
    except OperationalError as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}") from exc