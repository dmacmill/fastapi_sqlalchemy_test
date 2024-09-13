from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

######################################################################
# import settings
######################################################################
from .settings import DB_URI

######################################################################
#  create session with our settings
######################################################################
engine = create_engine(DB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # creates db sessions

Base = declarative_base()  # inherit from this in the /models dir
