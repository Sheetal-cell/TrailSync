from app.extensions import db

class TrekGallery(db.Model):

    __tablename__ = "trek_gallery"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    image = db.Column(
        db.String(255),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    trek = db.relationship(
        "Trek",
        back_populates="gallery"
    )