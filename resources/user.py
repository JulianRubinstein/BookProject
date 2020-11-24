from flask import request
from flask_restful import Resource
from bcrypt import hashpw, gensalt

from database.mongodb import users
from models.user import UserModel

class RegisterUser(Resource):
    def post(self):
        posted_data = request.get_json()

        if UserModel.registrate(posted_data) is not None:
            return UserModel.registrate(posted_data)

        hashed_password = hashpw(posted_data["password"].encode('utf8'), gensalt())
        posted_data["password"] = hashed_password

        users.insert(posted_data)

        return {"message":"user signed succesfuly", "status code":201}

class LogIn(Resource):
    def get(self):
        posted_data = request.get_json()

        if UserModel.authenticate(posted_data) is not None:
            return UserModel.authenticate(posted_data)

        return {"message":"succesfuly logged in", "status code":200}
