class BookModel:
    def validate_book(posted_data):
        if 'name' not in posted_data or 'author' not in posted_data:
            return {"message": "book must contain name and author", "status code":422}
        if (len(posted_data["name"]) == 0 or len(posted_data["author"]) == 0) :
            return {"message": "book must contain name and author", "status code":422}
