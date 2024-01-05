from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username: str, password: str, user_id: str, introduction: str=""):
        self.id = user_id
        self.username = username
        self.password = password
        self.introduction = introduction

    def __dict__(self):
        return {"_id": self.id, "username": self.username, "introduction": self.introduction}
