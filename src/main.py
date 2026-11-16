import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Employee Service")

EMPLOYEES_FILE = Path(__file__).with_name("employees.json")


class Employee(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


def read_employees():
    with EMPLOYEES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/employees")
def get_employees():
    return read_employees()


@app.get("/employees/{name}")
def get_employee(name: str):
    employees = read_employees()

    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(employee: Employee):
    employees = read_employees()
    employees.append(employee.model_dump())

    with EMPLOYEES_FILE.open("w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)

    return employee
