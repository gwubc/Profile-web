import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import mongomock

from GoalTracker.server import Server
from GoalTracker.UserManager import UserManager


class AuthTest(unittest.TestCase):

    def setUp(self):
        # Setup Flask test client and mock database
        mongo = mongomock.MongoClient()
        self.server = Server(mongo)
        self.app = self.server.app
        self.app.testing = True
        self.client = self.app.test_client()
        self.user_manager = UserManager(mongo)

    def test_index_not_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers['Location'])

    def test_index_login(self):
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('profile', response.headers['Location'])

    def test_profile_not_login(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.headers['Location'])

    def test_profile_login(self):
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)

    def test_update_introduction(self):
        new_introduction = "new_introduction"
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.client.put('/update_introduction', json={
            "introduction": new_introduction
        })
        user = self.user_manager.find_user_by_username('testuser')
        assert user.introduction == new_introduction


if __name__ == '__main__':
    unittest.main()
