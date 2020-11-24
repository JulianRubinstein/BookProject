from flask import request
from flask_restful import Resource
from bcrypt import hashpw, gensalt

from database.mongodb import users
from models.user import UserModel
import security

class RegisterUser(Resource):
    def post(self):
        posted_data = request.get_json()

        username, password = posted_data["username"], posted_data["password"]

        if UserModel.registrate(username, password) is not None:
            return UserModel.registrate(username, password)

        hashedPassword = hashpw(password.encode('utf8'), gensalt())
        users.insert({"username":username, "password":hashedPassword})

        return {"message":"user signed succesfuly", "status code":201}

class LogIn(Resource):
    def post(self):
        pass
