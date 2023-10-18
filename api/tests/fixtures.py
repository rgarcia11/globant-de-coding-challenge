import pytest

from api.challenge_app.app_factory import db, create_app
from api.challenge_app.models.employee_model import Employee


@pytest.fixture(scope="function")
def setup():
    app = create_app(config_name='test')
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
