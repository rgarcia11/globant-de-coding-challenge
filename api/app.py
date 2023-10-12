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


def insert_to_db(sql, data):
    try:
        db.session.execute(sa.text(sql), params=data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to insert data: {str(e)}"})


def handle_csv(data_structure, file, csv_header_row, batch_size, sql):
    if file:
        if file.filename.endswith('.csv'):
            csv_data = file.read().decode('utf-8').splitlines()
            if csv_header_row:
                csv_data = csv_data[1:]
            data = []
            for row in csv_data:
                values = row.split(',')
                data_object = {}
                for index, value in enumerate(data_structure):
                    data_object[value] = values[index]
                data.append(data_object)
                if len(data) == batch_size:
                    r = insert_to_db(sql, data)
                    if r:
                        return r
                    data = []
            if data:
                r = insert_to_db(sql, data)
                if r:
                    return r
            return jsonify({"message": "File uploaded and data inserted successfully"})
        else:
            return jsonify({"error": "Please upload a CSV file"})
    else:
        return jsonify({"error": "No file selected"})


@app.route('/upload_employees', methods=['POST'])
def upload_employees():
    file = request.files['csv_file']
    csv_header_row = True if request.form['csv_header_row'].lower() == 'true' else False
    try:
        batch_size = int(request.form['batch_size'])
        if batch_size > 1000:
            jsonify({"error": "The maximum batch size is 1000"})
    except ValueError:
        batch_size = 1000
    sql = """
    INSERT INTO employees (id, name, datetime, department_id, job_id)
    VALUES (:id, :name, :datetime, :department_id, :job_id);
    """
    data_structure = ["id", "name", "datetime", "department_id", "job_id"]
    return handle_csv(data_structure, file, csv_header_row, batch_size, sql)


@app.route('/upload_jobs', methods=['POST'])
def upload_jobs():
    file = request.files['csv_file']
    csv_header_row = True if request.form['csv_header_row'].lower() == 'true' else False
    try:
        batch_size = int(request.form['batch_size'])
        if batch_size > 1000:
            jsonify({"error": "The maximum batch size is 1000"})
    except ValueError:
        batch_size = 1000
    sql = """
    INSERT INTO jobs (id, job)
    VALUES (:id, :job);
    """
    data_structure = ["id", "job"]
    return handle_csv(data_structure, file, csv_header_row, batch_size, sql)


@app.route('/upload_departments', methods=['POST'])
def upload_departments():
    file = request.files['csv_file']
    csv_header_row = True if request.form['csv_header_row'].lower() == 'true' else False
    try:
        batch_size = int(request.form['batch_size'])
        if batch_size > 1000:
            jsonify({"error": "The maximum batch size is 1000"})
    except ValueError:
        batch_size = 1000
    sql = """
    INSERT INTO departments (id, department)
    VALUES (:id, :department);
    """
    data_structure = ["id", "department"]
    return handle_csv(data_structure, file, csv_header_row, batch_size, sql)


if __name__ == '__main__':
    app.run(debug=True)
