#!/bin/bash

# Run Black
echo "Running Black..."
pipenv run black --config pyproject.toml .

# Run Flake8
echo "Running Flake8..."
pipenv run flake8 --config .flake8 .

# Run MyPy
echo "Running MyPy..."
pipenv run mypy --config-file mypy.ini .

# Run Pytest
echo "Running Pytest..."
pipenv run pytest tests/
