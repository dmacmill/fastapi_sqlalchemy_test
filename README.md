# FastAPI SQLAlchemy Postgres 
A template crud app for future me to reference. Good for use as a template.


### Getting Started
`docker build -t fastapisqlalchemy .` to build image

then

`docker compose up`

then go to 0.0.0.0:8000/docs to use fastapi frontend

### TODO
 - needs github actions workflow to build and test in docker image
 - needs to use asyncpg instead of psycopg

### why this exists
I needed more practice with ORMs as using them is generally better practice than using inline SQL. So I will endeavor to write an ORM based backend now. Using [roughly this](https://fastapi.tiangolo.com/tutorial/sql-databases/#orms) app format.

I also wanted more projects on my page with docker compose to show off that I know that :P

