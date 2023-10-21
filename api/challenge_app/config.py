from google.cloud.sql.connector import Connector, IPTypes

# instance_connection_name = os.environ[
#     "INSTANCE_CONNECTION_NAME"
# ]  # i.e. 'project:region:instance'
# db_user = os.environ["DB_USER"]
# db_pass = os.environ["DB_PASS"]
# db_name = os.environ["DB_NAME"]
instance_connection_name = "propane-avatar-402503:us-central1:postgres"
db_user = "postgres"
db_pass = "password"
dev_db_name = "company_db"
test_db_name = "test_db"
ip_type = IPTypes.PUBLIC

connector = Connector()


def get_dev_conn():
    with Connector() as connector:
        conn = connector.connect(
            instance_connection_name,  # Cloud SQL Instance Connection Name
            "pg8000",  # driver
            user=db_user,
            password=db_pass,
            db=dev_db_name,
            ip_type=ip_type
        )
        return conn


def get_test_conn():
    with Connector() as connector:
        conn = connector.connect(
            instance_connection_name,  # Cloud SQL Instance Connection Name
            "pg8000",  # driver
            user=db_user,
            password=db_pass,
            db=test_db_name,
            ip_type=ip_type
        )
        return conn


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@/localhost:5543/company_db'
    # postgres+pg8000://<db_user>:<db_pass>@/<db_name>
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"


class DevelopmentConfig(Config):
    SQLALCHEMY_ENGINE_OPTIONS = {
        "creator": get_dev_conn
    }
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "creator": get_test_conn
    }
