FROM python:3.10-slim-buster

WORKDIR /usr/src/toxic-detector

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install poetry && poetry config virtualenvs.create false && poetry config installer.parallel false && poetry install --no-root

COPY app app/

CMD ["python", "-m", "app.main"]