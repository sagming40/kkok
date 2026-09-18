import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import get_settings
from app.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# alembic.ini의 sqlalchemy.url은 일부러 비워둔 상태 (비밀번호 commit 방지)
# 대신 app이 사용중인 .env → config.py 통로를 alembic도 그대로 빌려 사용한다.
#
# ⚠️ .replace("%", "%%")가 붙는 이유:
#    ini 파일에서 %는 "다른 값을 끼워넣어라"는 특수 기호다.   
#    DB 비밀번호에 %가 들어 있으면 alembic이 명령을 오인하여 오류가 발생한다.   
#    %를 %%로 변경하여 "글자 %"라는걸 명시한다.
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url.replace("%", "%%"))

# autogenerate가 compare할 "테이블 전체 설계도"
# app/models/__init__.py에 import된 model만 여기 모인다.
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        # compare_type=True:
        # default는 "column이 생성되었는지/아닌지"만 확인한다.
        # "Type이 바뀌었는지" 까지 감지한다. (예: VARCHAR(50) → VARCHAR(200))
        compare_type=True,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        # compare_type=True:
        # default는 "column이 생성되었는지/아닌지"만 확인한다.
        # "Type이 바뀌었는지" 까지 감지한다. (예: VARCHAR(50) → VARCHAR(200))
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
