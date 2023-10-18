from flask import Flask

from api.challenge_app.blueprints.departments_bp import departments_bp
from api.challenge_app.blueprints.employees_bp import employees_bp
from api.challenge_app.blueprints.jobs_bp import jobs_bp
from api.challenge_app.db_singleton import db


def create_app(config_name="development"):
    app = Flask(__name__)
    if config_name == "development":
        app.config.from_object("api.challenge_app.config.DevelopmentConfig")
    elif config_name == "test":
        app.config.from_object("api.challenge_app.config.TestConfig")
    else:
        raise ValueError("Invalid configuration name.")
    db.init_app(app)
    app.register_blueprint(employees_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(jobs_bp)
    return app
