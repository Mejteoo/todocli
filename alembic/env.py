from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Add src/ to path so we can import config
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")),
)
from config import load_config

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Load DSN from config and convert to SQLAlchemy URL
cfg = load_config()
# DSN like: "dbname=todo_db user=todo_user password=secret host=localhost port=5432"
parts = dict(item.split("=") for item in cfg["database"]["dsn"].split())
sqlalchemy_url = (
    f"postgresql+psycopg2://{parts['user']}:{parts['password']}@"
    f"{parts['host']}:{parts['port']}/{parts['dbname']}"
)
config.set_main_option("sqlalchemy.url", sqlalchemy_url)

# Manual migrations: no metadata for autogenerate
target_metadata = None


def run_migrations_offline():
    """
    Run migrations in 'offline' mode: generate SQL scripts without DB connection.
    """
    context.configure(
        url=sqlalchemy_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode: apply migrations to the database.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
