""" Models for Cupcake app. """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbx = db.session.execute

DEFAULT_CUPCAKE_URL = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """ Cupcake """

    __tablename__ = "cupcakes"

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True
    )

    flavor = db.mapped_column(
        db.String(50),
        nullable=False
    )

    size = db.mapped_column(
        db.String(15),
        nullable=False
    )

    rating = db.mapped_column(
        db.Integer,
        nullable=False
    )

    image_url = db.mapped_column(
        db.String(500),
        nullable=False,
        default=DEFAULT_CUPCAKE_URL
    )

    def serialize(self):
        """ Serialization to a dictionary. """

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image_url": self.image_url
        }
