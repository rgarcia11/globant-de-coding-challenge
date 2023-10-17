import sqlalchemy as sa
from flask_migrate import Migrate

from api.challenge_app.app_factory import create_app, db, db_uri
from api.challenge_app.blueprints.departments_bp import departments_bp
from api.challenge_app.blueprints.employees_bp import employees_bp
from api.challenge_app.blueprints.jobs_bp import jobs_bp

app = create_app()
app.register_blueprint(employees_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(jobs_bp)
Migrate(app, db)

# Configure the database connection
engine = sa.create_engine(db_uri)

if __name__ == '__main__':
    app.run(debug=True)
