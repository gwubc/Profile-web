import os

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ProfileWeb.UserManager import UserManager
from ProfileWeb.logger_config import logger


class Profile:
    """
    Manages user profiles for the application. This class creates and handles
    routes for viewing and updating user profiles.

    Attributes:
        blueprint (Blueprint): A Flask Blueprint object for routing.
        _user_manager (UserManager): An object to manage user-related operations like
                                    updating user information.

    Args:
        user_manager (UserManager): The UserManager instance to handle user operations.
        project_folder (str): The base directory of the project, used to set template and static folder paths.
    """

    def __init__(self, user_manager: UserManager, project_folder):
        self.blueprint = Blueprint("Profile", __name__, url_prefix="/",
                                   template_folder=os.path.join(project_folder, "templates"),
                                   static_folder=os.path.join(project_folder, "static"))

        self._user_manager = user_manager

        self.configure_routes()

    def configure_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index)
        self.blueprint.add_url_rule('/profile', 'profile', self.profile)
        self.blueprint.add_url_rule('/update_introduction', 'update_introduction', self.update_introduction, methods=['PUT'])

    def index(self):
        """
        Redirects to the appropriate view based on the authentication status of the user.
        Unauthenticated users are redirected to the login page, while authenticated users
        are redirected to their profile page.

        Returns:
            redirect: A redirection to either the profile page or the login page.
        """
        logger.debug(f"current_user.is_authenticated: {current_user.is_authenticated}, {current_user}")
        if current_user.is_authenticated:
            return redirect(url_for('.profile'))
        else:
            return redirect(url_for('Auth.login'))

    @login_required
    def profile(self):
        """
        Renders the profile page for an authenticated user. It provides user-specific information
        such as username and introduction.

        Returns:
            render_template: Renders the profile template populated with the user's information.
        """
        return render_template('profile.html', user_name=current_user.username, introduction=current_user.introduction)

    @login_required
    def update_introduction(self):
        """
        Handles the updating of a user's introduction. This method processes PUT requests
        containing the new introduction text and updates it in the user's profile.

        Returns:
            jsonify: A JSON response indicating the success or failure of the update operation.
        """
        try:
            new_introduction = request.json['introduction']
            self._user_manager.update_user_introduction(current_user.id, new_introduction)
            return jsonify({"success": True}), 200
        except AttributeError:
            return jsonify({"success": False}), 401
        except Exception:
            return jsonify({"success": False}), 405
