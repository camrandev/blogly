from models import DEFAULT_IMAGE_URL, User
from app import app, db
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_get_add_user(self):
        """ test 'add user' navigates and renders proper page"""
        with self.client as c:
            resp = c.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create a user", html)

    def test_redirect_from_home_to_users(self):
        """test the redirect from home to users"""
        with self.client as c:
            resp = c.get('/')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')

    def test_add_a_new_user(self):
        """test the add a new user route"""
        with self.client as c:
            resp = c.post('/users/new',
                          data={"first_name": "Lance",
                                "last_name": "Stephenson",
                                "image_url": None}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            # test if the new user exists in the DB
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Lance', html)

    def test_get_edit_user(self):
        """test that the edit user route renders the correct page"""
        with self.client as c:

            resp = c.get("/users/1/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Cancel', html)

    # def test_delete_user(self):
    #     with self.client as c:
    #         resp = c.post('/users/1/delete',
    #                       data={"first_name": "test1_first",
    #                             "last_name": "test2_last",
    #                             "image_url": None}, follow_redirects=True)
    #         # html = resp.get_data(as_text=True)

    # TODO: make sure deleted data is not in HTML

    #         # test if the new user exists in the DB
    #         all_users = db.query.all()
    #         self.assertEqual(len(all_users), 0)



