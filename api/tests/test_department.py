from datetime import datetime

from .fixtures import setup, setup_departments
from api.challenge_app.models.department_model import Department


def test_create_department(setup_departments):
    _, app = setup_departments

    new_department = Department(
        department="Test department!",
    )
    with app.app_context():
        client = app.test_client()
        response = client.post('/department', json=new_department.to_dict())

        assert response.status_code == 200


def test_get_single_department(setup_departments):
    test_department, app = setup_departments
    with app.app_context():
        client = app.test_client()
        response = client.get(f'/department?id={test_department.id}')

        assert response.status_code == 200

        response_json = response.get_json()
        assert response_json['id'] == test_department.id
        assert response_json['department'] == test_department.department


def test_get_all_departments(setup_departments):
    test_department, app = setup_departments
    with app.app_context():
        client = app.test_client()
        response = client.get('/departments')

        assert response.status_code == 200

        response_json = response.get_json()
        response_json = response_json[0]
        assert response_json['id'] == test_department.id
        assert response_json['department'] == test_department.department


def test_update_department(setup_departments):
    test_department, app = setup_departments

    new_department_data = {
        "department": "Edited Department 1"
    }
    with app.app_context():
        client = app.test_client()
        response = client.put(f'/department?id={test_department.id}', json=new_department_data)

        assert response.status_code == 200

        response = client.get(f'/department?id={test_department.id}')

        response_json = response.get_json()
        assert response_json['department'] == new_department_data['department']


def test_delete_single_department(setup_departments):
    test_department, app = setup_departments

    with app.app_context():
        client = app.test_client()
        response = client.delete(f'/department?id={test_department.id}')

        assert response.status_code == 200

        response = client.get(f'/department?id={test_department.id}')

        response_json = response.get_json()
        assert "Could not find" in response_json


def test_delete_all_departments(setup_departments):
    test_department, app = setup_departments

    with app.app_context():
        client = app.test_client()
        response = client.delete(f'/departments')

        assert response.status_code == 200

        response = client.get(f'/departments')

        response_json = response.get_json()
        assert response_json == []
