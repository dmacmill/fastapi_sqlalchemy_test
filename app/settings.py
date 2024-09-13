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


DB_URI = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    settings["POSTGRES_USER"],
    settings["POSTGRES_PASSWORD"],
    settings["POSTGRES_HOST"],
    settings["POSTGRES_PORT"],
    settings["POSTGRES_DB"])