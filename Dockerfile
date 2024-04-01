FROM python:3.12.1-slim


WORKDIR /code


ENV VIRTUAL_ENV=/var/venv/
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir  --upgrade -r  /code/requirements.txt


COPY ./app /code/app
COPY ./frontend /code/frontend/


CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]

