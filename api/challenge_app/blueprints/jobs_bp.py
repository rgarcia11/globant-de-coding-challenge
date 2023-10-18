import sqlalchemy
from flask import Blueprint, request, jsonify

from api.challenge_app.blueprints.utils import handle_csv
from api.challenge_app.db_singleton import db
from api.challenge_app.models.job_model import Job

jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route('/job', methods=['POST'])
def create_job():
    new_job_json = request.json
    new_job = Job.from_json(job_json=new_job_json)
    db.session.add(new_job)
    db.session.commit()
    return jsonify('Job inserted successfully')


@jobs_bp.route('/jobs', methods=['GET'])
def get_all_jobs():
    jobs = Job.query.all()
    return jsonify([job.to_dict() for job in jobs])


@jobs_bp.route('/job', methods=['GET'])
def get_job():
    job_id = request.args.get("id")
    job = Job.query.get(job_id)
    if job:
        return jsonify(job.to_dict())
    else:
        return jsonify(f'Could not find  job by id {job_id}')


@jobs_bp.route('/job', methods=['PUT'])
def update_job():
    job_id = request.args.get('id')
    updated_job = request.json
    try:
        job_to_update = Job.query.get(job_id)
        job_to_update.job = updated_job.get('job')
        db.session.commit()
        return jsonify('Job updated successfully')
    except (sqlalchemy.orm.exc.UnmappedInstanceError, AttributeError) as e:
        return jsonify(f'Could not update the job. Full error: {e}')


@jobs_bp.route('/job', methods=['DELETE'])
def delete_job():
    job_id = request.args.get('id')
    try:
        job_to_delete = Job.query.get(job_id)
        db.session.delete(job_to_delete)
        db.session.commit()
        return jsonify('Job deleted successfully')
    except sqlalchemy.orm.exc.UnmappedInstanceError as e:
        return jsonify(f'Could not find the job to delete. Full error: {e}')


@jobs_bp.route('/jobs', methods=['DELETE'])
def delete_all_job():
    Job.query.delete()
    db.session.commit()
    return jsonify('All jobs deleted successfully')


@jobs_bp.route('/jobs/upload', methods=['POST'])
def upload_jobs():
    file = request.files['csv_file']
    csv_header_row = True if request.form['csv_header_row'].lower() == 'true' else False
    try:
        batch_size = int(request.form['batch_size'])
        if batch_size > 1000:
            jsonify({"error": "The maximum batch size is 1000"})
    except ValueError:
        batch_size = 1000
    response = handle_csv(Job, file, csv_header_row, batch_size)
    return jsonify(response)
