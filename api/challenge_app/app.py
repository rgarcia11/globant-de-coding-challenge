# import sqlalchemy as sa
# from flask_migrate import Migrate

from api.challenge_app.app_factory import create_app  # , db

app = create_app(config_name='development')

# Migrate(app, db)

# Configure the database connection
# engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == '__main__':
    app.run(debug=True)
