# services/users/tests/test_users.py

import json
import unittest

from base import BaseTestCase
from project import db
from api.models import User
from utils import add_user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def login_the_user(self, admin=True):
        user = add_user('test', 'test@test.com', 'test')
        if admin == True:
            user.admin = True
        db.session.commit()
        resp_login = self.client.post(
                        '/auth/login',
                        data=json.dumps({
                                    'email': 'test@test.com',
                                    'password': 'test'
                                }),
                        content_type='application/json'
                    )
        token = json.loads(resp_login.data.decode())['auth_token']
        return token

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        token = self.login_the_user()
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': "bane",
                    "email": "cool@gmail.com",
                    "password": "greaterthaneight"
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('cool@gmail.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        token = self.login_the_user()
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        token = self.login_the_user()
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'awesomebane@gmail.com', 'password': 'greaterthaneight'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        token = self.login_the_user()
        self.client.post(
            '/users',
            data=json.dumps({'email': 'awesomebane@gmail.com', 'username': 'nmsbane', 'password': 'greaterthaneight'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'},
        )

        response = self.client.post(
            '/users',
            data=json.dumps({'email': 'awesomebane@gmail.com', 'username': 'nmsbane', 'password': 'greaterthaneight'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Sorry. That email already exists.', data['message'])
        self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('michael', 'michael@mherman.org', 'greaterthaneight')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@mherman.org', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('bane', 'bane@bane.org', 'greaterthaneight')
        add_user('fletcher', 'fletcher@notreal.com', 'greaterthaneight')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('success', data['status'])
            self.assertIn('fletcher@notreal.com', data['data']['users'][1]['email'])
            self.assertFalse(data['data']['users'][1]['admin'])
            self.assertFalse(data['data']['users'][0]['admin'])


    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no users have been
            added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)


    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been
            added to the database."""
        add_user('michael', 'michael@mherman.org', 'greaterthaneight')
        add_user('fletcher', 'fletcher@notreal.com', 'greaterthaneight')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'michael', response.data)
            self.assertIn(b'fletcher', response.data)


    def test_main_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                    '/',
                    data=dict(username='bane', email='bane@sonotreal.com', password='greaterthaneight'),
                    follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'bane', response.data)

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        token = self.login_the_user()
        with self.client:
            response = self.client.post('/users', data=json.dumps(dict(
                username='michael',
                email='bane@gmail.com'
            )), content_type='application/json',
            headers={'Authorization': f'Bearer {token}'},
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_inactive(self):
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                            '/auth/login',
                            data=json.dumps({
                                    'email': 'test@test.com',
                                    'password': 'test'
                                }),
                            content_type='application/json'
                        )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                            '/users',
                            data=json.dumps({
                                    'username': 'michael',
                                    'email': 'michael@sonotreal.com',
                                    'password': 'test'
                                    }),
                            content_type='application/json',
                            headers={'Authorization': f'Bearer {token}'}
                        )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)


    def test_add_user_not_admin(self):
        token = self.login_the_user(admin=False)
        response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@sonotreal.com',
                    'password': 'test'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'You do not have permission to do that.'
        )
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
   unittest.main()
