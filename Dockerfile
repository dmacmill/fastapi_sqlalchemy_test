FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
# tiangolo wants us to use something else, this is deprecated
# but there's no documentation on the new stuff, so whatever

COPY alembic/           /fastapi_sqlalchemy/alembic
COPY requirements.txt   /fastapi_sqlalchemy/
WORKDIR /fastapi_sqlalchemy/
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8000:8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
