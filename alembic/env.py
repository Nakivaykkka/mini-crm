from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from app.core.config import settings
from app.database import Base


env_path = Path(__file__).resolve().parent.parent / ".env"

loaded = load_dotenv(dotenv_path=env_path)

# PATH / ENV 
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Импорты из проекта 

#  Alembic Config 
config = context.config
fileConfig(config.config_file_name)

url_clean = settings.SQLALCHEMY_DATABASE_URL.encode("utf-8", "replace").decode("utf-8", "ignore")

config.set_main_option("sqlalchemy.url", url_clean)


# Установка строки подключения
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=settings.SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
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
