from datetime import datetime

from .fixtures import setup, setup_employees
from api.challenge_app.models.employee_model import Employee


def test_create_employee(setup_employees):
    _, app = setup_employees
    new_employee = Employee(
        name="Test Employee 1",
        datetime="2021-01-01T00:00:00Z",
        department_id=3,
        job_id=1,
    )
    with app.app_context():
        client = app.test_client()
        response = client.post('/employee', json=new_employee.to_dict())

        assert response.status_code == 200


def test_get_single_employee(setup_employees):
    test_employee, app = setup_employees
    with app.app_context():
        client = app.test_client()
        response = client.get(f'/employee?id={test_employee.id}')

        assert response.status_code == 200

        response_json = response.get_json()
        assert response_json['id'] == test_employee.id
        assert response_json['name'] == test_employee.name
        assert datetime.strptime(response_json['datetime'], '%a, %d %b %Y %H:%M:%S GMT') == test_employee.datetime
        assert response_json['department_id'] == test_employee.department_id
        assert response_json['job_id'] == test_employee.job_id


def test_get_all_employees(setup_employees):
    test_employee, app = setup_employees
    with app.app_context():
        client = app.test_client()
        response = client.get('/employees')

        assert response.status_code == 200

        response_json = response.get_json()
        response_json = response_json[0]
        assert response_json['id'] == test_employee.id
        assert response_json['name'] == test_employee.name
        assert datetime.strptime(response_json['datetime'], '%a, %d %b %Y %H:%M:%S GMT') == test_employee.datetime
        assert response_json['department_id'] == test_employee.department_id
        assert response_json['job_id'] == test_employee.job_id


def test_update_employee(setup_employees):
    test_employee, app = setup_employees

    new_employee_data = {
        "name": "Edited Employee 1"
    }
    with app.app_context():
        client = app.test_client()
        response = client.put(f'/employee?id={test_employee.id}', json=new_employee_data)

        assert response.status_code == 200

        response = client.get(f'/employee?id={test_employee.id}')

        response_json = response.get_json()
        assert response_json['name'] == new_employee_data['name']


def test_delete_single_employee(setup_employees):
    test_employee, app = setup_employees

    with app.app_context():
        client = app.test_client()
        response = client.delete(f'/employee?id={test_employee.id}')

        assert response.status_code == 200

        response = client.get(f'/employee?id={test_employee.id}')

        response_json = response.get_json()
        assert "Could not find" in response_json


def test_delete_all_employees(setup_employees):
    test_employee, app = setup_employees

    with app.app_context():
        client = app.test_client()
        response = client.delete(f'/employees')

        assert response.status_code == 200

        response = client.get(f'/employees')

        response_json = response.get_json()
        assert response_json == []
