from api.challenge_app.app_factory import db


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(255), nullable=True)

    def __init__(self, department, id=None):
        self.id = id
        self.department = department

    def __repr__(self):
        return f"Employee(id={self.id}, department='{self.department}'"

    def to_dict(self):
        return {
            'id':         self.id,
            'department': self.department,
        }

    @staticmethod
    def from_json(department_json):
        return Department(department=department_json.get('department'))

    @staticmethod
    def from_row(department_row):
        return Department(id=department_row[0], department=department_row[1])
