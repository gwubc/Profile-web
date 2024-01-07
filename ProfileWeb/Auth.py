import os

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from ProfileWeb.UserManager import UserManager
from ProfileWeb.logger_config import logger


class Auth:
    """
        Handles authentication for the application. This class creates and manages
        the routes for user registration, login, and logout.

        Attributes:
            blueprint (Blueprint): A Flask Blueprint object for routing.
            user_manager (UserManager): An object to manage user-related operations like
                                        finding, creating, and verifying users.

        Args:
            user_manager (UserManager): The UserManager instance to handle user operations.
            project_folder (str): The base directory of the project,
            used to set template and static folder paths.
        """

    def __init__(self, user_manager: UserManager, project_folder):
        self.blueprint = Blueprint("Auth", __name__, url_prefix="/",
                                   template_folder=os.path.join(project_folder, "templates"),
                                   static_folder=os.path.join(project_folder, "static"))

        self.user_manager = user_manager
        self.configure_routes()

    def configure_routes(self):
        """
        Configures URL routes for the blueprint.
        """

        self.blueprint.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.blueprint.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/logout', 'logout', self.logout, methods=['POST'])

    def register(self):
        """
        Handles the registration of a new user. This method is bound to the '/register'
        endpoint, and it processes POST requests with the user's username and password.

        Returns:
            jsonify: A JSON response containing the status of
            the registration and relevant messages.
        """
        logger.debug("create_user request.json, %s", request.json)

        username, password = request.json['username'], request.json['password']

        existing_user = self.user_manager.find_user_by_username(username)

        if existing_user is None:
            result = self.user_manager.create_user(username, password)
            login_user(self.user_manager.find_user_by_id(result))
            return jsonify({"success": True,
                            "message": "User created successfully",
                            "next": "/profile"}), 201

        return jsonify({"success": False, "message": "User already exists"}), 409

    def login(self):
        """
        Handles user login. For GET requests, it renders the login template.
        For POST requests, it processes the submitted username and password,
        authenticates the user, and manages the user session.

        Returns:
            jsonify or render_template:
                A JSON response for POST requests indicating login success or failure,
                or the login template for GET requests.
        """
        if request.method == 'POST':
            username, password = request.json['username'], request.json['password']
            user = self.user_manager.find_user_by_username(username)
            if user and self.user_manager.verify_password(user, password):
                login_user(user)
                logger.debug("login successful username: %s", username)
                return jsonify({"success": True, "message": "Success", "next": "/profile"}), 200
            logger.debug("login failed username: %s", username)
            return jsonify({"success": False, "message": "Invalid username or password"}), 401
        return render_template('auth.html')

    @login_required
    def logout(self):
        """
        Handles user logout. This method ends the user session and redirects to the login page.

        Returns:
            redirect: A redirection to the login page.
        """
        logout_user()
        return redirect(url_for('.login'))
