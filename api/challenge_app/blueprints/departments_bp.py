import json

import sqlalchemy
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from api.challenge_app.blueprints.utils import handle_csv, run_query
from api.challenge_app.db_singleton import db
from api.challenge_app.models.department_model import Department

departments_bp = Blueprint('departments', __name__)


@cross_origin()
@departments_bp.route('/department', methods=['POST'])
def create_department():
    new_department_json = request.json
    new_department = Department.from_json(department_json=new_department_json)
    db.session.add(new_department)
    db.session.commit()
    return jsonify('Department inserted successfully')


@cross_origin()
@departments_bp.route('/departments', methods=['GET'])
def get_all_departments():
    departments = Department.query.all()
    return jsonify([department.to_dict() for department in departments])


@cross_origin()
@departments_bp.route('/department', methods=['GET'])
def get_department():
    department_id = request.args.get("id")
    department = Department.query.get(department_id)
    if department:
        return jsonify(department.to_dict())
    else:
        return jsonify(f'Could not find  department by id {department_id}')


@cross_origin()
@departments_bp.route('/department', methods=['PUT'])
def update_department():
    department_id = request.args.get('id')
    updated_department = request.json
    try:
        department_to_update = Department.query.get(department_id)
        department_to_update.department = updated_department.get('department')
        db.session.commit()
        return jsonify('Department updated successfully')
    except (sqlalchemy.orm.exc.UnmappedInstanceError, AttributeError) as e:
        return jsonify(f'Could not update the department. Full error: {e}')


@cross_origin()
@departments_bp.route('/department', methods=['DELETE'])
def delete_department():
    department_id = request.args.get('id')
    try:
        department_to_delete = Department.query.get(department_id)
        db.session.delete(department_to_delete)
        db.session.commit()
        return jsonify('Department deleted successfully')
    except sqlalchemy.orm.exc.UnmappedInstanceError as e:
        return jsonify(f'Could not find the department to delete. Full error: {e}')


@cross_origin()
@departments_bp.route('/departments', methods=['DELETE'])
def delete_all_department():
    Department.query.delete()
    db.session.commit()
    return jsonify('All departments deleted successfully')


@cross_origin()
@departments_bp.route('/departments/upload', methods=['POST'])
def upload_departments():
    file = request.files['csv_file']
    csv_header_row = True if request.form['csv_header_row'].lower() == 'true' else False
    try:
        batch_size = int(request.form['batch_size'])
        if batch_size > 1000:
            jsonify({"error": "The maximum batch size is 1000"})
    except ValueError:
        batch_size = 1000
    response = handle_csv(Department, file, csv_header_row, batch_size)
    return jsonify(response)


@cross_origin()
@departments_bp.route('/departments/over_hiring_mean', methods=['GET'])
def departments_over_hiring_mean():
    year = request.args.get("year")
    error_message = "Failed to query database: {error_message}"
    sql = """
    WITH mean AS (
      SELECT AVG(cnt.cnt) AS mean
      FROM (
        SELECT COUNT (*) AS cnt
        FROM employees
        GROUP BY department_id
      ) cnt
    ),
    counts AS (
      SELECT d.id, d.department, COUNT(*) AS hired
      FROM employees e
      LEFT JOIN departments d ON e.department_id = d.id
      WHERE EXTRACT(year FROM datetime) = 2021
      GROUP BY d.id, d.department
    )
    SELECT counts.*
    FROM counts counts
    LEFT JOIN mean ON true
    WHERE counts.hired > mean.mean;
    """
    data = {
        "year": year
    }
    rows = run_query(sql, data, error_message)
    if not rows:
        return jsonify('Not enough data to compute!')

    try:
        results = [tuple(row) for row in rows]
        return json.dumps(results)
    except TypeError as e:
        return jsonify(f'Not enough data to compute. Full error: {e}')
