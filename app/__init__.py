from flask import Flask, render_template
from config import Config
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    @app.route("/")
    def home():
        return render_template("landing.html")
    return app