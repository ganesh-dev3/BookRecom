from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session, class_mapper
from model.tables import Books, Reviews
from sqlalchemy.sql import func

import json
import uuid




class CRUDService():
    def __init__(self, db_session:Session):
        self.db_session = db_session

    async def add_book(self, data):
        book = Books(slug=str(uuid.uuid4()), title = data.title,
                     author = data.author, genre = data.genre,
                     summary = data.summary, year_published = data.published_year)
        self.db_session.add(book)
        await self.db_session.flush()
        return "added"

    async def get_books(self):
        books = await self.db_session.execute(select(Books))#.order_by(Book.id)
        return [book.as_dict() for book in books.scalars().all()]

    def serialize(self, model):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        # first we get the names of all the columns on your model
        columns = [c.key for c in class_mapper(model.__class__).columns]
        # then we return their values in a dict
        return dict((c, getattr(model, '_' + c)) for c in columns)

    async def update_book(self, book_id, data = None):
        title=data.get('title')
        author=data.get('author')
        genre=data.get('genre')
        summary=data.get('summary')
        year_published=data.get('year_published')
        query = update(Books).where(Books.id == book_id)
        if title:
            query = query.values(title=title)
        if author:
            query = query.values(author=author)
        if genre:
            query = query.values(genre=genre)
        if summary:
            query = query.values(summary=summary)
        if year_published:
            query = query.values(year_published=year_published)

        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)
        return 'updated'

    async def delete_book(self, book_id):
        query = delete(Books).where(Books.id == book_id)
        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)
        return 'deleted'

    async  def get_reviews(self, book_id):
        print(book_id)
        books = await self.db_session.execute(select(Reviews).where(Reviews.book_id==book_id)) #.order_by(Book.id)
        return [book.as_dict() for book in books.scalars().all()]


    async def add_review(self, book_id, data):
        print(data)
        review = Reviews(slug=str(uuid.uuid4()), user_id = data.user_id,
                     review_text = data.review_text,
                     rating = data.rating, book_id = book_id)
        self.db_session.add(review)
        await self.db_session.flush()
        return "added"

    async  def summary(self, book_id):
        print(book_id)
        summary_data = await self.db_session.execute(select (Books.summary).where(Books.id==book_id))
        summary = summary_data.scalars().one()
        rating =  await self.db_session.execute(select (func.avg((Reviews.rating))).where(Reviews.book_id==book_id))
        return [summary, rating.scalars().one()]
