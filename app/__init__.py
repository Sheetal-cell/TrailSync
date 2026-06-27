from flask import Flask, render_template
from config import Config
from app.extensions import db
from app.models import User,Trek
from app.services.seed import create_admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/")
    def home():
        return render_template("landing.html")

    with app.app_context():
        print(db.Model.metadata.tables.keys())

        db.create_all()
        create_admin()

    return app