FROM python:3.13-alpine

LABEL maintainer="Nelya Parfenova <nelya.parfenova@gmail.com>"

RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    curl \
    build-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    POETRY_HOME="/application_root/poetry" \
    POETRY_CACHE_DIR="/application_root/.cache" \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=2.1.4

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}

RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

RUN mkdir ${POETRY_CACHE_DIR}

WORKDIR ${PYTHONPATH}

COPY pyproject.toml poetry.lock ./
COPY README.md ./
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./


COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN poetry install

RUN chown -R appuser:appgroup ${PYTHONPATH}

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000 || exit 1

# Use entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default to development mode
CMD ["development"]