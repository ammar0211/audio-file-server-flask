from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def init_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        db.create_all()  # Create sql tables for our data models
        if not os.path.exists("./song"):
            os.makedirs("./song")
        if not os.path.exists("./audiobook"):
            os.makedirs("./audiobook")
        if not os.path.exists("./podcast"):
            os.makedirs("./podcast")
        return app
