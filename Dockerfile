FROM python:3.9.1-slim AS base
WORKDIR /usr/src/app

COPY . .

# Environment Variables
ENV RELEASE_VERSION=0.1.9
ENV POETRY_VERSION=1.1.4
ENV VENV_PATH=/opt/venv


# Install system deps
RUN apt-get -y update && apt-get -y install curl


# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_VERSION=$POETRY_VERSION python
ENV PATH="$PATH:/root/.poetry/bin:$VENV_PATH/bin"
RUN python -m venv $VENV_PATH \
    && poetry config virtualenvs.create false

RUN poetry install

COPY vaccine_checker/ /usr/src/app/vaccine_checker/


CMD ["vaccine_checker/main.py"]
ENTRYPOINT ["python3"]