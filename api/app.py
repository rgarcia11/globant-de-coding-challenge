from flask import Flask, request, jsonify
import pandas as pd
from flask_migrate import Migrate
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database connection
db_uri = 'postgresql://username:password@localhost/company_db'
engine = create_engine(db_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
Migrate(app, db)


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    datetime = db.Column(db.DateTime, nullable=True)
    department_id = db.Column(db.Integer, nullable=True)
    job_id = db.Column(db.Integer, nullable=True)

    def __init__(self, name, datetime, department_id, job_id):
        self.name = name
        self.datetime = datetime
        self.department_id = department_id
        self.job_id = job_id

    def __repr__(self):
        return f"Employee(id={self.id}, name='{self.name}', datetime={self.datetime}, department_id={self.department_id}, job_id={self.job_id})"


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(255), nullable=True)

    def __init__(self, department):
        self.department = department

    def __repr__(self):
        return f"Employee(id={self.id}, department='{self.department}'"


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(255), nullable=True)

    def __init__(self, job):
        self.job = job

    def __repr__(self):
        return f"Employee(id={self.id}, job='{self.job}'"


if __name__ == '__main__':
    app.run(debug=True)
