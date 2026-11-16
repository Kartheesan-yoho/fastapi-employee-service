# FastAPI Employee Service

## Features

- GET /health - Check service health
- GET /employees - Get all employees
- GET /employees/{name} - Get an employee by name
- POST /employees - Create an employee

## Run the application

python -m uvicorn src.main:app --reload

## Run tests

python -m pytest -v

## Test coverage

python -m pytest --cov=src --cov-report=term-missing

## API documentation

http://127.0.0.1:8000/docs