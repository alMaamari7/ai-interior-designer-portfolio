"""Initial curated public portfolio schema.

Revision ID: 0001_public_schema
Revises:
"""

from alembic import op

from app.db.base import Base
import app.db.models  # noqa: F401

revision = "0001_public_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
