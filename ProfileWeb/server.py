import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo

from ProfileWeb.Auth import Auth
from ProfileWeb.UserManager import UserManager
from ProfileWeb.logger_config import logger


class Server:
    def __init__(self, mongo=None):
        project_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.app = Flask(__name__,
                         template_folder=os.path.join(project_folder, "templates"),
                         static_folder=os.path.join(project_folder, "static"))
        self.app.config["MONGO_URI"] = "mongodb://mongodb:27017/project"
        self.app.secret_key = "nyfper-1faTke-geqzyn"
        if mongo is None:
            mongo = PyMongo(self.app)
        self.mongo = mongo

        self._user_manager = UserManager(self.mongo)

        self._login_manager = LoginManager()
        self._login_manager.init_app(self.app)
        self._login_manager.login_view = 'Auth.login'
        self._login_manager.user_loader(self._user_manager.find_user_by_id)

        self.auth = Auth(self._user_manager, project_folder)
        self.app.register_blueprint(self.auth.blueprint)


server = Server()
app = server.app

if __name__ == '__main__':
    logger.debug("START")
    app.run(debug=True, host="0.0.0.0", port=5000)
