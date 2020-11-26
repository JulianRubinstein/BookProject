from bcrypt import hashpw, gensalt

from database.mongodb import users
import security

class UserModel:
    def __init__(self, username, password, email, **kwargs):
        self.username = username
        self.password = password
        self.email = email
        self.access = 1

    def to_admin(self):
        self.access = 2

    def to_dict(self):
        dict = {
        "username":self.username,
        "password":self.password,
        "email":self.email,
        "access":self.access
        }
        return dict

    def registrate(username, password, email, **kwargs):
        if (len(password) <= 5):
            return {"message":"password too short", "status code":401}

        if (len(username) <= 4):
            return {"message":"username too short", "status code":401}

        if "@" not in email or "." not in email:
            return {"message":"please enter valid email", "status code":401}

        if users.count_documents({'username': username}, limit = 1) != 0 :
            return {"message":"username already exists", "status code":403}

        if users.count_documents({'email': email}, limit = 1) != 0 :
            return {"message":"email already exists", "status code":403}

    def authenticate(username, password, **kwargs):
        if users.count_documents({'username': username}, limit = 1) == 0 :
            return {"message":"wrong username or password", "status code":401}

        hashed_password = users.find_one({"username":username})["password"]

        if hashpw(password.encode('utf8'), hashed_password) != hashed_password:
                return {"message":"wrong username or password", "status code":401}
