import io
import os
from datetime import datetime

from .fixtures import setup, setup_jobs
from api.challenge_app.models.job_model import Job

test_script_dir = os.path.dirname(os.path.abspath(__file__))


def test_create_job(setup_jobs):
    _, app = setup_jobs

    new_job = Job(
        job="Test job!",
    )
    with app.app_context():
        client = app.test_client()
        response = client.post('/job', json=new_job.to_dict())

        assert response.status_code == 200


def test_get_single_job(setup_jobs):
    test_job, app = setup_jobs
    with app.app_context():
        client = app.test_client()
        response = client.get(f'/job?id={test_job.id}')

        assert response.status_code == 200

        response_json = response.get_json()
        assert response_json['id'] == test_job.id
        assert response_json['job'] == test_job.job


def test_get_all_jobs(setup_jobs):
    test_job, app = setup_jobs
    with app.app_context():
        client = app.test_client()
        response = client.get('/jobs')

        assert response.status_code == 200

        response_json = response.get_json()
        response_json = response_json[0]
        assert response_json['id'] == test_job.id
        assert response_json['job'] == test_job.job


def test_update_job(setup_jobs):
    test_job, app = setup_jobs

    new_job_data = {
        "job": "Edited Job 1"
    }
    with app.app_context():
        client = app.test_client()
        response = client.put(f'/job?id={test_job.id}', json=new_job_data)

        assert response.status_code == 200

        response = client.get(f'/job?id={test_job.id}')

        response_json = response.get_json()
        assert response_json['job'] == new_job_data['job']


def test_delete_single_job(setup_jobs):
    test_job, app = setup_jobs

    with app.app_context():
        client = app.test_client()
        response = client.delete(f'/job?id={test_job.id}')

        assert response.status_code == 200

        response = client.get(f'/job?id={test_job.id}')

        response_json = response.get_json()
        assert "Could not find" in response_json


def test_delete_all_jobs(setup_jobs):
    test_job, app = setup_jobs

    with app.app_context():
        client = app.test_client()
        response = client.delete(f'/jobs')

        assert response.status_code == 200

        response = client.get(f'/jobs')

        response_json = response.get_json()
        assert response_json == []


def test_upload_jobs(setup_jobs):
    _, app = setup_jobs
    data_file = os.path.join(test_script_dir, "test_job_data.csv")

    with open(data_file, 'rb') as test_csv_file:
        data = {
            'csv_file':       (io.BytesIO(test_csv_file.read()), 'test.csv'),
            'csv_header_row': True,
            'batch_size':     10
        }
        with app.app_context():
            client = app.test_client()
            response = client.post('/jobs/upload', data=data, content_type='multipart/form-data')
            assert response.status_code == 200
