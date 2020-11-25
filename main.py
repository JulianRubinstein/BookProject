from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from models.user import UserModel
import resources.user as user
import resources.book as book
import resources.booklist as booklist
import security

app = Flask(__name__)
api = Api(app)

app.secret_key = security.secret_key
jwt = JWT(app, UserModel.authenticate, UserModel.identity)

api.add_resource(user.RegisterUser, "/registeruser")
api.add_resource(user.LogIn, "/login")
api.add_resource(book.SearchBooks, "/search")
api.add_resource(booklist.BookList, "/booklist")
api.add_resource(booklist.AddToList, "/addtolist")
api.add_resource(booklist.SearchList, "/searchlist")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
