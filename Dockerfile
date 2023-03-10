FROM node:19.3-slim as build

WORKDIR /react-app

COPY src/frontend/package.json .
RUN yarn install
COPY src/frontend .
RUN yarn run build

FROM python:3.10-slim

ENV POETRY_HOME /opt/poetry
ENV PATH $POETRY_HOME/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    PYTHONPYCACHEPREFIX=/tmp/cpython \
    POETRY_VIRTUALENVS_CREATE=false

RUN useradd -ms /bin/bash app && mkdir /app && mkdir /frontend && mkdir -p /opt && chmod 777 /opt

RUN apt update && apt install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python && \
    chmod -R 777 /opt

RUN apt update -y -q \
    && apt install -y -q --no-install-recommends build-essential

COPY pyproject.toml ./
RUN poetry install

WORKDIR /app
USER app
COPY --from=build /react-app/build /frontend
