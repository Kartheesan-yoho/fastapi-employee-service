import json

from fastapi.testclient import TestClient

from src import main

client = TestClient(main.app)


def setup_employees_file(tmp_path, monkeypatch):
    employees = [
        {"name": "John", "salary": 45000},
        {"name": "Priya", "salary": 60000},
    ]

    file_path = tmp_path / "employees.json"
    file_path.write_text(json.dumps(employees), encoding="utf-8")

    monkeypatch.setattr(main, "EMPLOYEES_FILE", file_path)
    return file_path


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_employees(tmp_path, monkeypatch):
    setup_employees_file(tmp_path, monkeypatch)

    response = client.get("/employees")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_employee_by_name(tmp_path, monkeypatch):
    setup_employees_file(tmp_path, monkeypatch)

    response = client.get("/employees/John")

    assert response.status_code == 200
    assert response.json()["name"] == "John"


def test_get_employee_not_found(tmp_path, monkeypatch):
    setup_employees_file(tmp_path, monkeypatch)

    response = client.get("/employees/Unknown")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_create_employee(tmp_path, monkeypatch):
    file_path = setup_employees_file(tmp_path, monkeypatch)

    response = client.post(
        "/employees",
        json={"name": "David", "salary": 55000},
    )

    assert response.status_code == 201
    assert response.json() == {"name": "David", "salary": 55000}

    saved_employees = json.loads(file_path.read_text(encoding="utf-8"))
    assert len(saved_employees) == 3


def test_create_employee_with_empty_name(tmp_path, monkeypatch):
    setup_employees_file(tmp_path, monkeypatch)

    response = client.post(
        "/employees",
        json={"name": "   ", "salary": 45000},
    )

    assert response.status_code == 422


def test_create_employee_with_invalid_salary(tmp_path, monkeypatch):
    setup_employees_file(tmp_path, monkeypatch)

    response = client.post(
        "/employees",
        json={"name": "David", "salary": 0},
    )

    assert response.status_code == 422
