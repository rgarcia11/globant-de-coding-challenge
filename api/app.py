from flask import Flask, request, jsonify
import pandas as pd
from flask_migrate import Migrate
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database connection
db_uri = 'postgresql://username:password@localhost/company_db'
engine = sa.create_engine(db_uri)
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


@app.route('/upload_employees', methods=['POST'])
def upload_employees():
    file = request.files['csv_file']
    if file:
        if file.filename.endswith('.csv'):
            csv_data = file.read().decode('utf-8').splitlines()
            for row in csv_data:
                values = row.split(',')
                sql = """
                INSERT INTO employees (id, name, datetime, department_id, job_id)
                VALUES (:id, :name, :datetime, :department_id, :job_id);
                """
                data = {
                    "id": values[0],
                    "name": values[1],
                    "datetime": values[2],
                    "department_id": values[3],
                    "job_id": values[4]
                }
                try:
                    db.session.execute(sa.text(sql), params=data)
                    db.session.commit()
                except Exception as e:
                    return jsonify({"error": f"Failed to insert data: {str(e)}"})
            return jsonify({"message": "File uploaded and data inserted successfully"})
        else:
            return jsonify({"error": "Please upload a CSV file"})
    else:
        return jsonify({"error": "No file selected"})


@app.route('/upload_jobs', methods=['POST'])
def upload_jobs():
    file = request.files['csv_file']
    if file:
        if file.filename.endswith('.csv'):
            csv_data = file.read().decode('utf-8').splitlines()
            for row in csv_data:
                values = row.split(',')
                sql = """
                INSERT INTO jobs (id, job)
                VALUES (:id, :job);
                """
                data = {
                    "id": values[0],
                    "job": values[1]
                }
                try:
                    db.session.execute(sa.text(sql), params=data)
                    db.session.commit()
                except Exception as e:
                    return jsonify({"error": f"Failed to insert data: {str(e)}"})
            return jsonify({"message": "File uploaded and data inserted successfully"})
        else:
            return jsonify({"error": "Please upload a CSV file"})
    else:
        return jsonify({"error": "No file selected"})


@app.route('/upload_departments', methods=['POST'])
def upload_departments():
    file = request.files['csv_file']
    if file:
        if file.filename.endswith('.csv'):
            csv_data = file.read().decode('utf-8').splitlines()
            for row in csv_data:
                values = row.split(',')
                sql = """
                INSERT INTO departments (id, department)
                VALUES (:id, :department);
                """
                data = {
                    "id": values[0],
                    "department": values[1],
                }
                try:
                    db.session.execute(sa.text(sql), params=data)
                    db.session.commit()
                except Exception as e:
                    return jsonify({"error": f"Failed to insert data: {str(e)}"})
            return jsonify({"message": "File uploaded and data inserted successfully"})
        else:
            return jsonify({"error": "Please upload a CSV file"})
    else:
        return jsonify({"error": "No file selected"})


if __name__ == '__main__':
    app.run(debug=True)
