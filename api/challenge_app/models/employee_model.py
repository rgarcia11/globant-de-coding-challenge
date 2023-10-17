from api.challenge_app.app_factory import db


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    datetime = db.Column(db.DateTime, nullable=True)
    department_id = db.Column(db.Integer, nullable=True)
    job_id = db.Column(db.Integer, nullable=True)

    def __init__(self, name, datetime, department_id, job_id, id=None):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.department_id = department_id
        self.job_id = job_id

    def __repr__(self):
        return f"Employee(id={self.id}, name='{self.name}', datetime={self.datetime}, department_id={self.department_id}, job_id={self.job_id})"

    def to_dict(self):
        return {
            'id':            self.id,
            'name':          self.name,
            'datetime':      self.datetime,
            'department_id': self.department_id,
            'job_id':        self.job_id
        }

    @staticmethod
    def from_json(employee_json):
        return Employee(
            name=employee_json.get('name'),
            datetime=employee_json.get('datetime'),
            department_id=employee_json.get('department_id'),
            job_id=employee_json.get('job_id')
        )

    @staticmethod
    def from_row(employee_row):
        return Employee(id=employee_row[0], name=employee_row[1], datetime=employee_row[2],
                        department_id=employee_row[3], job_id=employee_row[4])
