from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from .settings import DB_URI, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

######################################################################
#  create session with our settings
######################################################################
def ensure_database_exists():
    POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres"
    engine = create_engine(POSTGRES_URI, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
            {"dbname": POSTGRES_DB},
        ).scalar()
        if not result:
            conn.execute(text(f'CREATE DATABASE "{POSTGRES_DB}"'))
            print(f"database {POSTGRES_DB} has been created!")
        else:
            print(f"database {POSTGRES_DB} already exists")

ensure_database_exists()

engine = create_async_engine(DB_URI, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
