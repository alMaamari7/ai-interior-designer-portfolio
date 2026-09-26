import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.database import get_db
from app.main import app

# Import mapped classes so SQLAlchemy can resolve relationship targets.
from app.models.ai_analysis import AIAnalysis  # noqa: F401,E402
from app.models.budget import Budget  # noqa: F401,E402
from app.models.building_element import BuildingElement  # noqa: F401,E402
from app.models.confirmed_ai_analysis import ConfirmedAIAnalysis  # noqa: F401,E402
from app.models.constraint import Constraint  # noqa: F401,E402

from app.models.constraint_room_object import ConstraintRoomObject  # noqa: F401,E402
from app.models.design_goal import DesignGoal  # noqa: F401,E402
from app.models.design_request import DesignRequest  # noqa: F401,E402
from app.models.door import Door  # noqa: F401,E402
from app.models.floor import Floor  # noqa: F401,E402
from app.models.household import Household  # noqa: F401,E402
from app.models.image import Image  # noqa: F401,E402
from app.models.improvement_need import ImprovementNeed  # noqa: F401,E402
from app.models.room import Room  # noqa: F401,E402
from app.models.room_activity import RoomActivity  # noqa: F401,E402
from app.models.room_function import RoomFunction  # noqa: F401,E402
from app.models.room_object import RoomObject  # noqa: F401,E402
from app.models.user import User  # noqa: F401,E402
from app.models.wall import Wall  # noqa: F401,E402
from app.models.window import Window  # noqa: F401,E402


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    # These API tests exercise authentication and room ownership only. Build the
    # minimal SQLite schema they need instead of compiling PostgreSQL-specific
    # ARRAY columns from unrelated portfolio models.
    sqlite_tables = [
        Base.metadata.tables["users"],
        Base.metadata.tables["rooms"],
    ]
    Base.metadata.create_all(bind=engine, tables=sqlite_tables)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine, tables=sqlite_tables)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
