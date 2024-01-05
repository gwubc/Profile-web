import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import mongomock

from GoalTracker.server import Server


class AuthTest(unittest.TestCase):

    def setUp(self):
        # Setup Flask test client and mock database
        self.server = Server(mongo=mongomock.MongoClient())
        self.app = self.server.app
        self.app.testing = True
        self.client = self.app.test_client()

    def test_register(self):
        # Test user registration
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 201)

    def test_register_existing_user(self):
        # Test registration with an existing user
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })  # Register a user first
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 409)

    def test_login(self):
        with self.client as client:
            client.post('/register', json={
                'username': 'testuser',
                'password': 'testpass'
            })
            client.post('/logout')
            client.post('/login', json={
                'username': 'testuser',
                'password': 'testpass'
            })
            response = client.get('/profile')
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        with self.client as client:
            client.post('/register', json={
                'username': 'testuser',
                'password': 'testpass'
            })
            client.post('/logout')
            response = client.get('/profile')
            self.assertEqual(response.status_code, 302)
            self.assertIn('login', response.headers['Location'])

    def test_index_unauthenticated(self):
        # Test index route without authentication
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers['Location'])


if __name__ == '__main__':
    unittest.main()
