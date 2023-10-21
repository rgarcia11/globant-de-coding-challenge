import os

from flask_migrate import Migrate

from api.challenge_app.app_factory import create_app, config_blueprints
from api.challenge_app.db_singleton import db

app = create_app(config_name='development')
config_blueprints(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
