FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libx11-6 \
    libxext-dev \
    libxrender-dev \
    libxinerama-dev \
    libxi-dev \
    libxrandr-dev \
    libxcursor-dev \
    libxtst-dev \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

RUN pip install pipenv

# Copy requirements
COPY Pipfile Pipfile

RUN pipenv lock
RUN pipenv install --system

WORKDIR /app/src
COPY src /app/src/

# Set up entry point
CMD [ "python", "src/main.py" ]