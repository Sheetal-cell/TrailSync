from flask import render_template
from flask_login import login_required, current_user

from app.trekker import trekker_bp
from app.models import Trek

@trekker_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "TREKKER":
        return "Unauthorized", 403

    treks = Trek.query.all()

    print("Treks found:", len(treks))
    for t in treks:
        print(t.trek_name, t.status)

    return render_template(
        "trekker/dashboard.html",
        treks=treks
    )

@trekker_bp.route("/trek/<int:trek_id>")
@login_required
def trek_details(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    return render_template(
        "trekker/trek_details.html",
        trek=trek
    )