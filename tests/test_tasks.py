import os
import unittest
from datetime import datetime, date

from project import app, db, bcrypt
from project.__config import basedir
from project.models import Task, User


TEST_DB = 'test.db'


class TasksTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.app.post('/', data=dict(
            email=email, password=password), follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('/add', data=dict(
            name='Go to the bank',
            due_date=date.today(),
            priority='1',
            posted_date=datetime.utcnow(),
            status='1'
        ), follow_redirects=True)

    def create_admin_user(self):
        new_user = User(
            name='Superman',
            email='admin@realpython.com',
            password='allpowerful',
        )
        db.session.add(new_user)
        db.session.commit()

    def test_logged_in_users_can_access_tasks_page(self):
        self.register(
            'Fletcher', 'fletcher@realpython.com', 'python101', 'python101'
        )
        self.login('fletcher@realpython.com', 'python101')
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task', response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('/tasks', follow_redirects=True)
        self.assertIn(b'Login First', response.data)

    def test_users_can_add_tasks(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('/tasks', follow_redirects=True)
        response = self.create_task()
        self.assertIn(
            b'New Task Added!', response.data
        )

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('/tasks', follow_redirects=True)
        response = self.app.post('/add', data=dict(
            name='Go to the bank',
            due_date='',
            priority='1',
            posted_date='02/05/2014',
            status='1'
        ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        response = self.app.get("/complete/1", follow_redirects=True)
        self.assertIn(b'Task marked completed', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        response = self.app.get("/delete/1", follow_redirects=True)
        self.assertIn(b'Task Deleted', response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('fletcher@realpython.com', 'python101')
        self.app.get('/tasks', follow_redirects=True)
        response = self.app.get("/complete/1", follow_redirects=True)
        self.assertNotIn(
            b'Task marked completed', response.data
        )
        self.assertIn(
            b'Only assigned user or admin can complete the task.', response.data
        )

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('fletcher@realpython.com', 'python101')
        self.app.get('/tasks', follow_redirects=True)
        response = self.app.get("/delete/1", follow_redirects=True)
        self.assertIn(
            b'Only assigned user or admin can delete the task.', response.data
        )

    def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('/tasks', follow_redirects=True)
        response = self.app.get("/complete/1", follow_redirects=True)
        self.assertNotIn(
            b'Only assigned user or admin can complete the task.', response.data
        )

    def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('/tasks', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('/tasks', follow_redirects=True)
        response = self.app.get("/delete/1", follow_redirects=True)
        self.assertNotIn(
            b'Only assigned user or admin can delete the task.', response.data
        )

    def test_string_reprsentation_of_the_task_object(self):

        from datetime import date
        db.session.add(
            Task(
                "Run around in circles",
                date(2020, 7, 25),
                10,
                1,
                1,
                datetime.utcnow()
            )
        )

        db.session.commit()

        tasks = db.session.query(Task).all()
        for task in tasks:
            self.assertEqual(task.name, 'Run around in circles')

    def test_username_displayed_after_login(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('michael@realpython.com', 'python')
        response = self.app.get('/tasks', follow_redirects=True)
        self.assertIn(b'Welcome, Michael!', response.data)

    def test_users_cannot_see_task_modify_links_for_tasks_not_created_by_them(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.register(
            'Fletcher', 'fletcher@realpython.com', 'python101', 'python101'
        )
        response = self.login('Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        self.assertNotIn(b'Mark as complete', response.data)
        self.assertNotIn(b'Delete', response.data)

    def test_users_can_see_task_modify_links_for_tasks_created_by_them(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.login('michael@realpython.com', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.register('Fletcher', 'fletcher@realpython.com', 'python101', 'python101')
        self.login('fletcher@realpython.com', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/', response.data)


if __name__ == "__main__":
    unittest.main()
