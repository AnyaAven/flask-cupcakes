from unittest import TestCase

from app import app
from models import db, dbx, Cupcake

from unittest import TestCase

from app import app
from models import db, dbx, Cupcake

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# To run the tests, you must provide a "test database", since these tests
# delete & recreate the tables & data. In your shell:
#
# Do this only once:
#   $ createdb cupcakes_test
#
# To run the tests using that test data:
#   $ DATABASE_URL=postgresql:///cupcakes_test python3 -m unittest

if not app.config['SQLALCHEMY_DATABASE_URI'].endswith("_test"):
    raise Exception("\n\nMust set DATABASE_URL env var to db ending with _test")

# NOW WE KNOW WE'RE IN THE RIGHT DATABASE, SO WE CAN CONTINUE

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.app_context().push()
db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        dbx(db.delete(Cupcake))
        db.session.commit()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [{
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            cupcake_id = resp.json['cupcake']['id']

            # don't know what ID we'll get, make sure it's an int
            self.assertIsInstance(cupcake_id, int)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": cupcake_id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg"
                }
            })

            q = db.select(Cupcake)
            self.assertEqual(len(dbx(q).scalars().all()), 2)
