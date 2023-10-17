# app/employees/views.py
import json

import sqlalchemy
from flask import Blueprint, request, jsonify

from api.challenge_app.app_factory import db
from api.challenge_app.blueprints.utils import handle_csv, run_query
from api.challenge_app.models.employee_model import Employee

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/employee', methods=['POST'])
def create_employee():
    new_employee_json = request.json
    new_employee = Employee.from_json(employee_json=new_employee_json)
    db.session.add(new_employee)
    db.session.commit()
    return jsonify('Employee inserted successfully')


@employees_bp.route('/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])


@employees_bp.route('/employee', methods=['GET'])
def get_employee():
    employee_id = request.args.get("id")
    employee = Employee.query.get(employee_id)
    if employee:
        return jsonify(employee.to_dict())
    else:
        return jsonify(f'Could not find  employee by id {employee_id}')


@employees_bp.route('/employee', methods=['PUT'])
def update_employee():
    employee_id = request.args.get('id')
    updated_employee = request.json
    try:
        employee_to_update = Employee.query.get(employee_id)
        employee_to_update.employee = updated_employee.get('employee')
        db.session.commit()
        return jsonify('Employee updated successfully')
    except (sqlalchemy.orm.exc.UnmappedInstanceError, AttributeError) as e:
        return jsonify(f'Could not update the employee. Full error: {e}')


@employees_bp.route('/employee', methods=['DELETE'])
def delete_employee():
    employee_id = request.args.get('id')
    try:
        employee_to_delete = Employee.query.get(employee_id)
        db.session.delete(employee_to_delete)
        db.session.commit()
        return jsonify('Employee deleted successfully')
    except sqlalchemy.orm.exc.UnmappedInstanceError as e:
        return jsonify(f'Could not find the employee to delete. Full error: {e}')


@employees_bp.route('/employees', methods=['DELETE'])
def delete_all_employee():
    Employee.query.delete()
    db.session.commit()
    return jsonify('All employees deleted successfully')


@employees_bp.route('/employees/upload', methods=['POST'])
def upload_employees():
    file = request.files['csv_file']
    csv_header_row = True if request.form['csv_header_row'].lower() == 'true' else False
    try:
        batch_size = int(request.form['batch_size'])
        if batch_size > 1000:
            jsonify({"error": "The maximum batch size is 1000"})
    except ValueError:
        batch_size = 1000
    response = handle_csv(Employee, file, csv_header_row, batch_size)
    return jsonify(response)


@employees_bp.route('/employees/hired_by_quarter', methods=['GET'])
def employees_hired():
    year = request.args.get("year")
    error_message = "Failed to query database: {error_message}"
    sql = """
    SELECT
      d.department,
      j.job,
      COUNT(*) FILTER (WHERE EXTRACT(quarter FROM datetime) = 1) AS Q1,
      COUNT(*) FILTER (WHERE EXTRACT(quarter FROM datetime) = 2) AS Q2,
      COUNT(*) FILTER (WHERE EXTRACT(quarter FROM datetime) = 3) AS Q3,
      COUNT(*) FILTER (WHERE EXTRACT(quarter FROM datetime) = 4) AS Q4
    FROM employees e
    LEFT JOIN departments d ON e.department_id = d.id
    LEFT JOIN jobs j ON e.job_id = j.id
    WHERE EXTRACT(year FROM datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY department ASC, job ASC;
    """
    data = {
        "year": year
    }
    rows = run_query(sql, data, error_message)
    results = [tuple(row) for row in rows]
    return json.dumps(results)
