from flask import request
from flask_restful import Resource
from pymongo import MongoClient
from bcrypt import hashpw, gensalt

import security

client = MongoClient(security.password)
db = client.objects
users = db["users"]

class UserMethods:
    def insert(postedData):
        username, password = postedData["username"], postedData["password"]

        if (len(password) <= 5):
            return {"message":"password too short", "status code":401}

        if users.count_documents({'username': username}, limit = 1) != 0 :
            return {"message":"username already exists", "status code":403}

        #Hash password and append user
        hashedPassword = hashpw(password.encode('utf8'), gensalt())
        users.insert({"username":username, "password":hashedPassword})

        return {"message":"user signed succesfuly", "status code":201}

    def authenticate(postedData):
        username, password = postedData["username"], postedData["password"]

        if users.count_documents({'username': username}, limit = 1) == 0 :
            return False
        else:
            hashedPassword = users.find_one({"username":username})["password"]
            if hashpw(password.encode('utf8'), hashedPassword) == hashedPassword:
                return True
            else:
                return False

class RegisterUser(Resource):
    def post(self):
        #Get data
        postedData = request.get_json()
        
        #Validating user and appending if valid
        insertuser = UserMethods.insert(postedData)

        return insertuser
