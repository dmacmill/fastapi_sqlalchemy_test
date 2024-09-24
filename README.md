# FastAPI SQLAlchemy Asyncpg Postgres 
### but smaller hopefully

I learned my lesson from the [https://github.com/dmacmill/fastapi_backend](https://github.com/dmacmill/fastapi_backend)
- that ORMs are important for mostly CRUD projects in that 
1) pydantic can't fill the role of SQLAlchemy when dealing with database models. pydantic only does app modeling.
2) ORMs can help a little with SQL injection (still need to do input sanitation though)
3) ORMs are things you gotta design around, not just squeeze in last minute into a project.
4) ORMs will probably do SQL better than you, n00b.

So I will endeavor to write an ORM based backend now. Using [https://fastapi.tiangolo.com/tutorial/sql-databases/#orms](roughly this) app format.

### Getting Started
`docker build -t fastapisqlalchemy .` to build image

then

`docker compose up`

then go to 0.0.0.0:8000/docs to use fastapi frontend