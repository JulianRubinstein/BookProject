class BookModel:
    def validate_book(name= "", authors = [], **kwargs):
        if len(name) == 0 or len(authors) == 0:
            return {"message": "book must contain name and author", "status code":422}
