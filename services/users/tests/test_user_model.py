# services/users/tests/test_user_model.py

import unittest

from project import db
from api.models import User
from base import BaseTestCase
from sqlalchemy.exc import IntegrityError
from utils import add_user

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('justausername', 'test@gmail.com')

        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justausername')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('justatest', 'test@test.com1')

        duplicate_user = User(
            username='justatest',
            email='test@test2.com',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('justatest', 'test@test.com')

        duplicate_user = User(
            username='justanothertest',
            email='test@test.com',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('justatest', 'test@gmail.com')
        self.assertTrue(isinstance(user.to_json(), dict))


if __name__ == '__main__':
    unittest.main()
