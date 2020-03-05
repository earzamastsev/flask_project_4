from flask import Flask
from models import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

from views import *

if __name__ == '__main__':
    app.run()
