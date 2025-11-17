from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings

#: SQLAlchemy engine for PostgreSQL database.
#:
#: Configuration:
#: - pool_pre_ping: Test connections before use (detect stale connections)
#: - pool_size: 10 connections maintained in pool
#: - max_overflow: 20 additional connections when pool exhausted
#:
#: Total max connections: pool_size + max_overflow = 30
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

#: Session factory for creating database sessions.
#:
#: Configuration:
#: - autocommit=False: Requires explicit db.commit()
#: - autoflush=False: Manual control over when changes flushed to DB
#: - bind=engine: Sessions use the configured engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency that provides database session with cleanup.

    Yields SQLAlchemy Session object and ensures proper cleanup via finally block.
    Used throughout FastAPI endpoints via Depends(get_db) for database access.

    Yields:
        Session: SQLAlchemy session for database operations.

    Usage in Endpoints:
        from fastapi import Depends
        from sqlalchemy.orm import Session
        from surveys_service.db.session import get_db

        @router.get("/items")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items

    Note:
        - Session automatically closed in finally block
        - Changes must be explicitly committed with db.commit()
        - Rollback automatic on exception (no explicit rollback needed)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """Test database connectivity with simple query.

    Executes "SELECT 1" to verify database is accessible and responsive.
    Used by application entrypoint to ensure database available before startup.

    Raises:
        SQLAlchemyError: If database connection fails or query execution fails.
    """
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
