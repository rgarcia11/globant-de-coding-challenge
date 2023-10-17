from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_uri = 'postgresql://postgres:password@localhost:5543/company_db'


def create_app():
    app = Flask(__name__)
    # ? TODO: include initialization from config app.config.from_pyfile(config_filename)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.init_app(app)

    return app
