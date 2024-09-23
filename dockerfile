FROM python:3.12.6-slim AS python-base

# Poetry configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge --auto-remove -y curl \
    && rm -rf /var/lib/apt/lists/*

# Copy poetry.lock* in case it doesn't exist in the repo
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Install runtime deps
RUN poetry install --no-dev

# Copy application code
WORKDIR /app
COPY . .

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]