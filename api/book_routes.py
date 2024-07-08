from book_dataclass import *
from quart import Blueprint, request
from auth import api_key_required

from quart_schema import validate_request, validate_response, validate_headers, security_scheme

books_page = Blueprint('books', __name__)

from model.sql_connect import get_session, engine, Base
from model.add_records import CRUDService

@validate_response(AddBookModel)
#@validate_headers(Headers)
@books_page.route('/books', methods=["GET"])
@api_key_required()
async def get():
    async with get_session() as session:
        async with session.begin():
            books = CRUDService(session)
            return await books.get_books()

#@validate_headers(Headers)
@books_page.route('/books', methods=["POST"])
@validate_request(AddBookModel)
@api_key_required()
async def post(data):
    #data = request.get_json()
    async with get_session() as session:
        async with session.begin():
            books = CRUDService(session)
            return await books.add_book(data)


#@validate_headers(Headers)
@validate_request(UpdateBookModel)
@books_page.route('/books/<book_id>', methods=["PUT"])
@api_key_required()
async def put(book_id):
    print(book_id, 'bookd id')
    data = await request.get_json()
    async with get_session() as session:
        async with session.begin():
            books = CRUDService(session)
            return await books.update_book(book_id, data)


@books_page.route('/books/<book_id>', methods=["DELETE"])
@api_key_required()
async def delete(book_id):
    print(book_id, 'bookd id')
    data = await request.get_json()
    async with get_session() as session:
        async with session.begin():
            books = CRUDService(session)
            return await books.delete_book(book_id)

@books_page.route('/reviews/<book_id>', methods=["GET"])
@api_key_required()
async def reviews_get(book_id):
    print(book_id)
    async with get_session() as session:
        async with session.begin():
            books = CRUDService(session)
            return await books.get_reviews(book_id)

#@validate_headers(Headers)
@books_page.route('/reviews/<book_id>', methods=["POST"])
@validate_request(AddReviewModel)
@api_key_required()
async def reviews_post(book_id, data):
    #data = request.get_json()
    print(data, book_id)
    async with get_session() as session:
        async with session.begin():
            books = CRUDService(session)
            return await books.add_review(book_id, data)

@books_page.route('/summary/<book_id>', methods=["GET"])
@api_key_required()
async def summary_rating(book_id):
    #data = request.get_json()
    print(book_id)
    async with get_session() as session:
        async with session.begin():
            books = CRUDService(session)
            return await books.summary(book_id)

@books_page.route('/recommendations', methods=["GET"])
@api_key_required()
async def get_recommendations():
    #data = request.get_json()
    pass

@books_page.route('/generate_summary', methods=["POST"])
#@validate_request(AddReviewModel)
@api_key_required()
async def generate_summary(data):
    #data = request.get_json()
    pass