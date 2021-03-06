FROM python:3.9.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/home/appuser/web/

WORKDIR ${WORKDIR}

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock ${WORKDIR}

RUN poetry export -f requirements.txt --output requirements.txt && \
    pip install -r requirements.txt

COPY . ${WORKDIR}

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser ${WORKDIR}

USER appuser

EXPOSE 8000
