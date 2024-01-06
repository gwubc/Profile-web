import unittest
import mongomock
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from ProfileWeb.UserManager import UserManager


class UserManagerTest(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager(mongomock.MongoClient())

    def test_create_user(self):
        username = "testuser"
        password = "testpass"
        user_id = self.user_manager.create_user(username, password)
        assert user_id is not None

    def test_create_user_invalid_name(self):
        username = ""
        password = "testpass"
        try:
            self.user_manager.create_user(username, password)
            self.fail("Except ValueError")
        except ValueError:
            pass
        except:
            self.fail("Except ValueError")

    def test_create_user_invalid_password(self):
        username = "testuser"
        password = ""
        try:
            self.user_manager.create_user(username, password)
            self.fail("Except ValueError")
        except ValueError:
            pass
        except:
            self.fail("Except ValueError")

    def test_create_user_with_same_username(self):
        username = "testuser"
        password = "testpass"
        self.user_manager.create_user(username, password)
        try:
            self.user_manager.create_user(username, password)
            self.fail("Except ValueError")
        except ValueError:
            pass
        except:
            self.fail("Except ValueError")

    def test_find_user_by_username(self):
        username = "testuser"
        password = "testpass"
        self.user_manager.create_user(username, password)
        user = self.user_manager.find_user_by_username(username)
        assert user is not None
        assert user.__dict__()["username"] == username

    def test_find_user_by_username_not_found(self):
        username = "testuser"
        password = "testpass"
        self.user_manager.create_user(username, password)
        user = self.user_manager.find_user_by_username(username + "_")
        assert user is None

    def test_find_user_by_id(self):
        username = "testuser"
        password = "testpass"
        id = self.user_manager.create_user(username, password)
        user = self.user_manager.find_user_by_id(id)
        assert user is not None
        assert user.__dict__()["username"] == username

    def test_find_user_by_id_not_found(self):
        username = "testuser"
        password = "testpass"
        id = self.user_manager.create_user(username, password)
        user = self.user_manager.find_user_by_id("".join(["0" for _ in id]))
        assert user is None

    def test_update_user(self):
        username = "testuser"
        password = "testpass"
        introduction = "new introduction"
        id = self.user_manager.create_user(username, password)
        self.user_manager.update_user_introduction(id, introduction)
        user = self.user_manager.find_user_by_id(id)
        assert user.introduction == introduction


if __name__ == '__main__':
    unittest.main()
