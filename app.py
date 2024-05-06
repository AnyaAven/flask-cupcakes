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
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', "my_favorite_color_is_qjol")


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
    Pass in to the body {id, flavor, size, rating, image_url}
    Everything is required except the image_url which is optional.
    Pass "image_url": null and image_url will be set to the default image.

    Return JSON {cupcake: {id, flavor, size, rating, image_url}}.
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json["image_url"]

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


################################################################################
# UPDATE AND DELETE CUPCAKES

@app.patch("/api/cupcakes/<int:cc_id>")
def update_cupcake(cc_id):
    """ Update cupcake data
    Pass in to the body {id, flavor, size, rating, image_url}
    Everything is optional.
    The properties will remain the same if no value is sent in the body.

    Return JSON of newly updated cupcake
       {cupcake: {id, flavor, size, rating, image_url}}
    """

    cupcake = db.get_or_404(Cupcake, cc_id)

    # Gather updated data sent or default to current data of the cupcake
    # Then update cupcake
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image_url = request.json.get("image_url", cupcake.image_url)

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.delete("/api/cupcakes/<int:cc_id>")
def delete_cupcake(cc_id):
    """ Delete cupcake data from DB

    Return JSON of deleted cupcake {deleted: [cupcake-id]}
    """

    cupcake = db.get_or_404(Cupcake, cc_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({"deleted": cc_id})


