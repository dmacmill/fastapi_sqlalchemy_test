from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from starlette.config import Config, environ


######################################################################
# import settings
######################################################################
if 'TESTING' in environ:
    config = Config('test.env')
else:
    import asyncpg
    config = Config('.env')

settings = {
    "POSTGRES_USER": config("POSTGRES_USER", cast=str, default="postgres"),
    "POSTGRES_PASSWORD": config("POSTGRES_PASSWORD", cast=str, default="postgres"),
    "POSTGRES_DB": config("POSTGRES_DB", cast=str, default="postgres"),
    "POSTGRES_HOST": config("POSTGRES_HOST", cast=str, default="localhost"),
    "POSTGRES_PORT": config("POSTGRES_PORT", cast=str, default="5432"),
    "POSTGRES_ECHO": config("POSTGRES_ECHO", cast=bool, default=True),
    "POSTGRES_POOL_SIZE": config("POSTGRES_POOL_SIZE", cast=int, default=5),
}


# TODO: hookup asyncpg somehow
# "postgresql+asyncpg://..."
connection_string = "postgresql://{}:{}@{}:{}/{}".format(
    settings["POSTGRES_USER"],
    settings["POSTGRES_PASSWORD"],
    settings["POSTGRES_HOST"],
    settings["POSTGRES_PORT"],
    settings["POSTGRES_DB"])

######################################################################
#  create session with our settings
######################################################################
engine = create_engine(connection_string)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # creates db sessions

Base = declarative_base()  # inherit from this in the /models dir
