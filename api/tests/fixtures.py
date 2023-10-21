import pytest

from api.challenge_app.app_factory import db, create_app, config_blueprints
from api.challenge_app.models.department_model import Department
from api.challenge_app.models.employee_model import Employee
from api.challenge_app.models.job_model import Job


@pytest.fixture(scope="function")
def setup():
    app = create_app(config_name='test')
    config_blueprints(app)
    yield app, db


@pytest.fixture(scope="function")
def setup_employees(setup):
    app, _ = setup

    employee1 = Employee(
        name="Test Employee 1",
        datetime="2021-01-01T00:00:00Z",
        department_id=3,
        job_id=1,
    )
    with app.app_context():
        db.create_all()
        db.session.add(employee1)
        db.session.commit()
        db.session.refresh(employee1)
        yield employee1, app

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def setup_jobs(setup):
    app, _ = setup

    job1 = Job(
        job="Test job!"
    )
    with app.app_context():
        db.create_all()
        db.session.add(job1)
        db.session.commit()
        db.session.refresh(job1)
        yield job1, app

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def setup_departments(setup):
    app, _ = setup

    department1 = Department(
        department="Test department!"
    )
    with app.app_context():
        db.create_all()
        db.session.add(department1)
        db.session.commit()
        db.session.refresh(department1)
        yield department1, app

        db.session.remove()
        db.drop_all()
