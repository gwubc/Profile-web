import typing

from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from ProfileWeb.User import User
from ProfileWeb.logger_config import logger


class UserManager:
    """
    Manages user-related operations in the application. This class interacts
    with the MongoDB database to perform user creation, searching, and updating.

    Attributes:
        mongo: An instance of the MongoDB client used to interact with the database.
        _users: A reference to the 'users' collection in the MongoDB database.

    Args:
        mongo: The MongoDB client provided to interact with the database.
    """

    def __init__(self, mongo):
        self.mongo = mongo
        self._users = self.mongo.db.users

    def create_user(self, username: str, password: str) -> str:
        """
        Creates a new user with the given username and password.

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.

        Returns:
            str: The string representation of the ObjectId of the newly created user.

        Raises:
            ValueError: If the username already exists or if username or password is not provided.
        """

        if not username or not password:
            raise ValueError("Username and password are required")

        if self.find_user_by_username(username):
            raise ValueError("Username exists")

        hashed_password = generate_password_hash(password)
        result = self._users.insert_one({'username': username, 'password': hashed_password, 'introduction': ""})
        return str(result.inserted_id)

    def _create_user(self, user_data):
        """
        Private helper method to create a user object from the provided user data.

        Args:
            user_data: The data dictionary containing user information from the database.

        Returns:
            User: An instance of the User class populated with the user's data.
        """
        return User(user_data["username"], user_data["password"], str(user_data["_id"]), user_data["introduction"])

    def find_user_by_username(self, username: str) -> typing.Union[User, None]:
        """
        Finds a user by their username.

        Args:
            username (str): The username of the user to find.

        Returns:
            User or None: The User object if found, otherwise None.
        """
        user = None
        user_data = self._users.find_one({'username': username})
        logger.debug(f"find_user_by_username: {username}")
        if user_data:
            logger.debug(f"find_user_by_username success name: {username}")
            user = self._create_user(user_data)
        return user

    def find_user_by_id(self, user_id: typing.Union[str, ObjectId]) -> typing.Union[User, None]:
        """
        Finds a user by their unique ObjectId.

        Args:
            user_id: The ObjectId of the user to find.

        Returns:
            User or None: The User object if found, otherwise None.
        """

        user = None
        user_data = self._users.find_one({'_id': ObjectId(user_id)})
        logger.debug(f"find_user_by_id: {user_id}")
        if user_data:
            logger.debug(f"find_user_by_id success id: {user_id}")
            user = self._create_user(user_data)
        return user

    def update_user_introduction(self, user_id: typing.Union[str, ObjectId], introduction: str):
        """
        Updates the introduction text for a user.

        Args:
            user_id (str): The ObjectId of the user as a string.
            introduction (str): The new introduction text to be set for the user.

        Returns:
            bool: True if the update was successful, raises an exception otherwise.

        Raises:
            AttributeError: If the user with the specified user_id is not found.
            Exception: If any other error occurs during the update.
        """

        logger.debug(f"update_user: {user_id}, introduction: {introduction}")

        user = self.find_user_by_id(user_id)
        if not user:
            logger.debug(f"User: {user_id} not found")
            raise AttributeError(f"User: {user_id} not found")

        try:
            result = self._users.update_one({"_id": ObjectId(user_id)}, {"$set": {"introduction": introduction}})
            if result.modified_count == 0:
                logger.debug(f"update_user: {user_id} failed")
                raise Exception("Not modified")
            return True

        except Exception as e:
            logger.debug(f"update_user: {user_id} failed {e}")
            raise Exception(e)

    def verify_password(self, user: User, password: str):
        """
        Verifies a user's password.

        Args:
            user (User): The User object whose password needs to be verified.
            password (str): The password to check against the user's stored hash.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        return check_password_hash(user.password, password)
