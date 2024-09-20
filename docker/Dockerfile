FROM python:3.12

WORKDIR /code

RUN apt-get -y update
RUN apt-get -y upgrade

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# configure poetry and copy poetry toml and lock files
RUN pip install poetry
COPY ./poetry.lock ./pyproject.toml /code/
# install dependencies directly in container without creating an environment
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction

EXPOSE 8001

# copy the code
COPY . /code/

CMD [ "bin/bash", "-c", "fastapi run src/geomatrix/main.py --port 8001" ]