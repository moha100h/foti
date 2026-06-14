"""Alembic environment — uses psycopg2 (sync) for migrations.
The bot itself uses asyncpg at runtime; Alembic uses psycopg2 only during migration runs.
"""
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import all models so Alembic can detect schema changes
from football_bot.database import Base  # noqa: F401
import football_bot.models.user        # noqa: F401
import football_bot.models.match       # noqa: F401
import football_bot.models.prediction  # noqa: F401
import football_bot.models.team        # noqa: F401

config = context.config

# Allow DATABASE_URL override from environment (psycopg2 variant)
db_url = os.getenv("ALEMBIC_DATABASE_URL") or config.get_main_option("sqlalchemy.url")
config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


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
