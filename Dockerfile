FROM python:3.10

COPY /app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY app /app
WORKDIR /app

# run the FastAPI app with gunicorn, using uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]