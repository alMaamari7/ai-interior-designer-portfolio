"""Compatibility re-export for the canonical database configuration.

New code should import database objects from app.db.database.
"""

from app.db.database import SessionLocal, engine, get_db

__all__ = ["engine", "SessionLocal", "get_db"]
