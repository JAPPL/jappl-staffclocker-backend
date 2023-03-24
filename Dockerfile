FROM python:3.9.16-slim

ENV user=jappl
ENV gid=1001
ENV uid=1001
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.1.13 \
    POETRY_HOME="/home/$user/.poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false

ENV PATH="$POETRY_HOME/bin:$PATH"

# Create user (for security)
RUN addgroup --gid $gid $user && adduser --disabled-password --gecos "" --uid $uid --gid $gid $user
RUN chown -R $user:$user /home/$user

WORKDIR /home/$user/app

# install build package
RUN apt-get update && apt-get upgrade -y
RUN apt-get install --no-install-recommends -y \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# install poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false

# install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry check
RUN poetry install --no-dev

# Clean up build packages
RUN rm -rf ~/.cache/pypoetry/{cache,artifacts} ${POETRY_HOME}
RUN apt-get remove -y curl git && \
    apt-get clean && \
    apt-get autoremove -y

# set up project
COPY . .
RUN python manage.py collectstatic  --no-input --clear \
    && chown -R $uid:$gid $HOME \
    && chmod -R o-rwx,g-wx .\
    && chmod +x docker-entrypoint.sh manage.py \
    && rm -rf poetry.lock pyproject.toml \

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh", "gunicorn", "jappl_staffclocker_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout 600", "--preload"]
