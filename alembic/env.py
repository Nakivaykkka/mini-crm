from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.core.database import Base
from app.client.models import Client
from app.user.models import User
from app.security.enums import UserRole
from app.deal.models import Deal

import os
from dotenv import load_dotenv
load_dotenv()

import os






# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if DATABASE_URL.startswith("postgresql+asyncpg"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    

if not DATABASE_URL:
    raise ValueError("SQLALCHEMY_DATABASE_URL is not set!")
    
config.set_main_option("sqlalchemy.url", DATABASE_URL)
    
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
target_metadata = Base.metadata
# Interpret the config file for Python logging.
# This line sets up loggers basically.


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
            
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
        
     
       

    

