import os
import unittest
from project import app, db
from project.__config import basedir
from project.models import User

TEST_DB = 'test.db'


class MainTests(unittest.TestCase):

    def setUp(self):
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.app.post('/', data=dict(email=email, password=password), follow_redirects=True)

    def test_404_error(self):
        response = self.app.get('/blah-blah')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Looks like invalid link address', response.data)

    def test_500_error(self):
        invalid_user = User(name='blah', email='blah@unknown.com', password='superblah')
        db.session.add(invalid_user)
        db.session.commit()
        self.assertRaises(ValueError, self.login, 'blah@unknown.com', 'superblah')
        try:
            response = self.login('blah@unknown.com', 'superblah')
            self.assertEqual(response.status_code, 500)
        except ValueError:
            pass

if __name__ == '__main__':
    unittest.main()
