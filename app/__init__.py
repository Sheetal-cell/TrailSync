from flask import Flask, render_template
from config import Config
from app.extensions import db
from app.models import User,Trek
from app.services.seed import create_admin
from app.extensions import login_manager
from app.auth import auth_bp
from app.admin import admin_bp
from app.staff import staff_bp
from app.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "warning"


    @app.route("/")
    def home():
        return render_template("landing.html")

    with app.app_context():
        print(db.Model.metadata.tables.keys())

        db.create_all()
        create_admin()

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(user_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))