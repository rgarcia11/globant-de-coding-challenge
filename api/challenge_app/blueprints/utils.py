import sqlalchemy as sa
from flask import jsonify

from api.challenge_app.db_singleton import db


def run_query(sql, data, error_message):
    try:
        cur = db.session.execute(sa.text(sql), params=data)
        return cur.fetchall()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": error_message.format(error_message=e)})


def handle_csv(model, file, csv_header_row, batch_size):
    if file:
        if file.filename.endswith('csv'):
            csv_data = file.read().decode('utf-8').splitlines()
            if csv_header_row:
                csv_data = csv_data[1:]

            instance_batch = []

            for row in csv_data:
                values = row.split(',')
                instance = model.from_row(
                    values
                )
                instance_batch.append(instance)
                if len(instance_batch) >= batch_size:
                    db.session.add_all(instance_batch)
                    db.session.commit()
                    instance_batch = []

            if instance_batch:
                db.session.add_all(instance_batch)
                db.session.commit()
            return {"message": "File uploaded and data inserted successfully"}
        else:
            return {"error": "Please upload a CSV file"}
    else:
        return {"error": "No file selected"}
