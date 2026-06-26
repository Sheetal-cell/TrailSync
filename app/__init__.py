from flask import Flask, render_template
from config import Config
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/")
    def home():
        return render_template("landing.html")

    with app.app_context():
        db.create_all()

    return app