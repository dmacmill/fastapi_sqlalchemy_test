# FastAPI SQLAlchemy Postgres 
A template crud app for future me to reference. Good for use in small-scale applications.


### Getting Started
`docker compose build`

then

`docker compose up`

then 127.0.0.1:8000/docs to test the backend.

# run tests
Make sure you use the test-docker-compose.yml build
`docker compose -f test-docker-compose.yml`
`docker compose -f test-docker-compose up`

then

`docker exec -it fastapi_sqlalchemy-fastapi-1 pytest app/test/`