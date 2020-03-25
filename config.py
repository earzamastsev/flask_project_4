DEBUG = False
SECRET_KEY = 'my_secret_key'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:eugene123@127.0.0.1:5432/flask_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
