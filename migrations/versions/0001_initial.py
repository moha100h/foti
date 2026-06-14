"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-14
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("telegram_id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("first_name", sa.String(64), nullable=False, server_default=""),
        sa.Column("last_name", sa.String(64), nullable=True),
        sa.Column("username", sa.String(64), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_banned", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("external_id", sa.String(64), unique=True, nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("country", sa.String(64), nullable=True),
        sa.Column("league", sa.String(128), nullable=True),
        sa.Column("elo_rating", sa.Float(), nullable=True, server_default="1500.0"),
        sa.Column("fifa_ranking", sa.Integer(), nullable=True),
        sa.Column("form", sa.String(10), nullable=True),
        sa.Column("goals_scored", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("goals_conceded", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("external_id", sa.String(64), unique=True, nullable=False),
        sa.Column("home_team", sa.String(128), nullable=False),
        sa.Column("away_team", sa.String(128), nullable=False),
        sa.Column("home_score", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("away_score", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("status", sa.String(32), nullable=True, server_default="scheduled"),
        sa.Column("league", sa.String(128), nullable=True),
        sa.Column("season", sa.String(16), nullable=True),
        sa.Column("kickoff_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("minute", sa.Integer(), nullable=True),
        sa.Column("home_xg", sa.Float(), nullable=True),
        sa.Column("away_xg", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_matches_external_id", "matches", ["external_id"])
    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("match_id", sa.Integer(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("prediction_type", sa.String(64), nullable=False),
        sa.Column("home_win_prob", sa.Float(), nullable=True),
        sa.Column("draw_prob", sa.Float(), nullable=True),
        sa.Column("away_win_prob", sa.Float(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.String(16), nullable=True, server_default="medium"),
        sa.Column("explanation", sa.String(1024), nullable=True),
        sa.Column("status", sa.String(16), nullable=True, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_predictions_match_id", "predictions", ["match_id"])


def downgrade() -> None:
    op.drop_table("predictions")
    op.drop_table("matches")
    op.drop_table("teams")
    op.drop_table("users")
