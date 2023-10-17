from api.challenge_app.app_factory import db


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(255), nullable=True)

    def __init__(self, job, id=None):
        self.id = id
        self.job = job

    def __repr__(self):
        return f"Job(id={self.id}, job='{self.job}'"

    def to_dict(self):
        return {
            'id':  self.id,
            'job': self.job
        }

    @staticmethod
    def from_json(job_json):
        return Job(
            job=job_json.get('job')
        )

    @staticmethod
    def from_row(job_row):
        return Job(id=job_row[0], job=job_row[1])
