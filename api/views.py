from flask_home import book_ns
from flask_restx import Api, Resource, fields
from model.tables import Books, db

@book_ns.route('/books', methods=["GET", "POST"])
class Getbooks(Resource):
    def get(self):
        books = Books.query.all()
        return [book.__dict__ for book in books]

    def post(self):
        pass