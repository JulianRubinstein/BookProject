from pymongo import MongoClient

import security

client = MongoClient(security.password)
db = client.objects
books = db["books"]

class BookModel:
    def getbook(posted_data):
        #Checking if book is in database (only book name and book author can uniquely identify a book)
        return_data = books.find_one({ "$and" : [ {'name':posted_data["name"]} , {'author':posted_data["author"]} ] }, {"_id":0} )

        if return_data == None :
            return {"message":"no such book", "status code":200}

        return {"book":return_data, "message":"succesful", "status code":200}

    def addbook(posted_data):
        #Checking book is valid (only book name and book author can uniquely identify a book)
        if 'name' not in posted_data or 'author' not in posted_data:
            return {"message": "book must contain name and author", "status code":422}
        if (len(posted_data["name"]) == 0 or len(posted_data["author"]) == 0) :
            return {"message": "book must contain name and author", "status code":422}

        #Checking if book already exists
        if books.count_documents({ "$and" : [ {'name':posted_data["name"]} , {'author':posted_data["author"]} ] }, limit = 1) != 0 :
            return {"message":"book already exists", "status code":403}

        books.insert(posted_data)

        return {"message":"added book", "status code":200}

    def searchbook(posted_data):
            #Querying data from database using a regular expression (regex)
            return_data = list(books.find({ "$or" : [ {'name':{"$regex":posted_data["search"]}} , {'author':{"$regex":posted_data["search"]}} ] }, {"_id":0} ))

            if len(return_data) == 0:
                return {"message":"no books found", "status code":200}

            #Returning a list of only book names and authors
            book_list = [{"name":book_index["name"], "author":book_index["author"]} for book_index in return_data]

            return {"books":book_list, "message":"succesful", "status code":200}
