from pymongo import MongoClient
from bcrypt import hashpw, gensalt

import security

client = MongoClient(security.password)
db = client.objects
users = db["users"]

class UserModel:
    def insert(posted_data):
        username, password = posted_data["username"], posted_data["password"]

        if (len(password) <= 5):
            return {"message":"password too short", "status code":401}

        if users.count_documents({'username': username}, limit = 1) != 0 :
            return {"message":"username already exists", "status code":403}

        hashedPassword = hashpw(password.encode('utf8'), gensalt())
        users.insert({"username":username, "password":hashedPassword})

        return {"message":"user signed succesfuly", "status code":201}

    def authenticate(posted_data):
        username, password = posted_data["username"], posted_data["password"]

        if users.count_documents({'username': username}, limit = 1) == 0 :
            return {"message":"wrong username or password", "status code":401}
        else:
            hashedPassword = users.find_one({"username":username})["password"]
            if hashpw(password.encode('utf8'), hashedPassword) == hashedPassword:
                return {"message":"logged in succesfuly", "status code":200}
            else:
                return {"message":"wrong username or password", "status code":401}
