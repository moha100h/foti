"""Alembic env — uses psycopg2 (sync) for migrations.
Does NOT import football_bot.config to avoid pydantic validation at migration time.
Reads .env directly with python-dotenv.
"""
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load .env from project root (two levels up from migrations/)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Build psycopg2 URL from environment
# ALEMBIC_DATABASE_URL takes priority; fallback: convert asyncpg URL to psycopg2
_db_url = os.getenv("ALEMBIC_DATABASE_URL") or os.getenv("DATABASE_URL", "")
if "+asyncpg" in _db_url:
    _db_url = _db_url.replace("+asyncpg", "+psycopg2")

# Import models AFTER env is loaded (no pydantic validation triggered here)
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, BigInteger, Integer, String, Boolean, Float, DateTime,
    ForeignKey, func, true, false
)

# Minimal Base — mirrors football_bot.database.Base
Base = declarative_base()

# Mirror models inline to avoid importing football_bot package
class User(Base):
    __tablename__ = "users"
    telegram_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(64), nullable=False, server_default="")
    last_name = Column(String(64), nullable=True)
    username = Column(String(64), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=true())
    is_banned = Column(Boolean, nullable=False, server_default=false())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(64), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    country = Column(String(64), nullable=True)
    league = Column(String(128), nullable=True)
    elo_rating = Column(Float, nullable=True, server_default="1500.0")
    fifa_ranking = Column(Integer, nullable=True)
    form = Column(String(10), nullable=True)
    goals_scored = Column(Integer, nullable=True, server_default="0")
    goals_conceded = Column(Integer, nullable=True, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(64), unique=True, nullable=False)
    home_team = Column(String(128), nullable=False)
    away_team = Column(String(128), nullable=False)
    home_score = Column(Integer, nullable=True, server_default="0")
    away_score = Column(Integer, nullable=True, server_default="0")
    status = Column(String(32), nullable=True, server_default="scheduled")
    league = Column(String(128), nullable=True)
    season = Column(String(16), nullable=True)
    kickoff_time = Column(DateTime(timezone=True), nullable=True)
    minute = Column(Integer, nullable=True)
    home_xg = Column(Float, nullable=True)
    away_xg = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    prediction_type = Column(String(64), nullable=False)
    home_win_prob = Column(Float, nullable=True)
    draw_prob = Column(Float, nullable=True)
    away_win_prob = Column(Float, nullable=True)
    confidence = Column(Float, nullable=False)
    risk_level = Column(String(16), nullable=True, server_default="medium")
    explanation = Column(String(1024), nullable=True)
    status = Column(String(16), nullable=True, server_default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

target_metadata = Base.metadata

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url with the psycopg2 URL
config.set_main_option("sqlalchemy.url", _db_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
