FROM python:3.11-slim AS os-cache

ENV TZ=UTC
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y build-essential

WORKDIR /app

# FIXME: README.md seemed to be required here but I'm not sure why!
COPY poetry.lock pyproject.toml Makefile README.md ./

RUN pip install "poetry~=1.2"

FROM os-cache AS image

COPY poker ./poker
RUN make install-prod

FROM os-cache AS test-image

COPY setup.cfg ./
COPY poker ./poker
COPY tests ./tests
RUN make install
