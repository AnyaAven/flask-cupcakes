"""Flask app for Cupcakes"""

import os

from flask import Flask, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, dbx, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

app.config['SECRET_KEY'] = "my_favorite_color_is_qjol"

# Having the Debug Toolbar show redirects explicitly is often usefu#l;
# however, if you want to turn it off, you can uncomment this line:
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

@app.get("/api/cupcakes")
def get_cupcakes_data():
    """ Get all cupcakes data and return JSON
    {cupcakes: [{id, flavor, size, rating, image_url}, ...]}.
    """

    q = db.select(Cupcake).order_by(Cupcake.rating)
    cupcakes = dbx(q).scalars().all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get("/api/cupcakes/<int:cc_id>")
def get_cupcake_data(cc_id):
    """ Get cupcake data and return JSON
    {cupcake: {id, flavor, size, rating, image_url}}.
    """
    cupcake = db.get_or_404(Cupcake, cc_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post("/api/cupcakes")
def create_cupcake():
    """ Create a cupcake.
    Return JSON {cupcake: {id, flavor, size, rating, image_url}}.
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json.get("image_url")

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image_url=image_url
        )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)
