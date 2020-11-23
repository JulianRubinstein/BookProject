from flask import request
from flask_restful import Resource

from models.user import UserModel

class RegisterUser(Resource):
    def post(self):
        posted_data = request.get_json()

        username, password = posted_data["username"], posted_data["password"]

        if registrate() is not None:
            return registrate()

        hashedPassword = hashpw(password.encode('utf8'), gensalt())
        users.insert({"username":username, "password":hashedPassword})

        return {"message":"user signed succesfuly", "status code":201}

class LogIn(Resource):
    def post(self):
        pass
