FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/
RUN pipenv sync --system

COPY . .

WORKDIR /app/src

CMD python main.py