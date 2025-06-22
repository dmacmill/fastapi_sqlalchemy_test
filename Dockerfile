FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
# switch over to updated base image someday

WORKDIR /app

COPY requirements.txt  .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY app/ app/
EXPOSE 8000:8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
