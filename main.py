from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from bcrypt import hashpw, gensalt

client = MongoClient('mongodb+srv://Julian:toniii75@cluster0.qpdwa.mongodb.net/users?retryWrites=true&w=majority')
db = client.objects

users = db["users"]
books = db["books"]
bookLists = db["book lists"]

app = Flask(__name__)
api = Api(app)

def authenticate(username, password):
    if users.count_documents({'username': username}, limit = 1) == 0 :
        return False
    else:
        hashedPassword = users.find_one({"username":username})["password"]
        if hashpw(password.encode('utf8'), hashedPassword) == hashedPassword:
            return True
        else:
            return False

def bookValidity(postedData):
        if "name" or "author" not in postedData:
            return False

        if (len(postedData["name"]) == 0 or len(postedData["author"]) == 0) :
            return False

        return True

class RegisterUser(Resource):
    def post(self):
        #Get data
        postedData = request.get_json()
        username, password= postedData["username"], postedData["password"]

        #Check if password long enough
        if (len(password) <= 5):
            return {"message":"password too short", "status code":401}

        #Check if user already exists
        if users.count_documents({'username': username}, limit = 1) != 0 :
            return {"message":"username already exists", "status code":403}

        #Hash password
        hashedPassword = hashpw(password.encode('utf8'), gensalt())

        #Append user
        users.insert({
            "username":username,
            "password":hashedPassword,
            })

        return {"message":"user signed succesfuly", "status code":201}

class Book(Resource):
    def get(self):
        #Get data
        postedData = request.get_json()

        #Querying the data
        returnData = books.find_one({ "$and" : [ {'name':postedData["name"]} , {'author':postedData["author"]} ] }, {"_id":0} )

        if returnData == None :
            return {"message":"no such book", "status code":200}

        return {"book":returnData, "message":"succesful", "status code":200}

    def post(self):
        #Get data
        postedData = request.get_json()

        #Checking book is valid
        bookValid = bookValidity(postedData)
        if not bookValid:
            return {"message": "book must contain name and author", "status code":422}

        #Checking if book already exists
        if books.count_documents({ "$and" : [ {'name':postedData["name"]} , {'author':postedData["author"]} ] }, limit = 1) != 0 :
            return {"message":"book already exists", "status code":403}

        #Add item
        books.insert(postedData)

        return {"message":"added book", "status code":200}

class Search(Resource):
    def get(self):
        #Get data
        postedData = request.get_json()

        #Querying data from database
        returnData = list(books.find({ "$or" : [ {'name':{"$regex":postedData["search"]}} , {'author':{"$regex":postedData["search"]}} ] }, {"_id":0} ))

        #Checking if no results
            if len(returnData) == 0:
                return {"message":"no books found", "status code":200}

        return {"books":returnData, "message":"succesful", "status code":200}

class BookList(Resource):
    def post(self):
        pass

    def get(self):
        pass


# class postInterest(Resource):
#     def post(self):
#
#         #Get data
#         postedData = request.get_json()
#         username = postedData["username"]
#         password = postedData["password"]
#         interest = postedData["interest"]
#
#         #Authenticate Info
#         authenticated = authenticate(username, password)
#         if not authenticated:
#             return {"message":"wrong username or password", "status code":401}
#
#         #Add Interest
#         db.users.update({"username":username}, {"$push": {"interests":interest} })
#
#         return {"message":"added interest", "status code":200}
#
# class getInterests(Resource):
#     def post(self):
#
#         #Get data
#         postedData = request.get_json()
#         username = postedData["username"]
#         password = postedData["password"]
#
#         #Authenticate Info
#         authenticated = authenticate(username, password)
#         if not authenticated:
#             return {"message":"wrong username or password", "status code":401}
#
#         #Return interests
#         interests = db.users.find_one({"username":username})["interests"]
#
#         return {"interests":interests, "status code":200}

api.add_resource(RegisterUser, "/registeruser")
api.add_resource(Book, "/book")
api.add_resource(Search, "/search")
# api.add_resource(postInterest, "/postInterest")
# api.add_resource(getInterests, "/getInterests")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
