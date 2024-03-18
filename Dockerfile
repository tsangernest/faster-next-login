FROM python:3.12.1-slim


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir  --upgrade -r  /code/requirements.txt


COPY ./app /code/app
COPY ./frontend /code/frontend/


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
