import sys
sys.path.append('../BooksRecom')

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from model.sql_connect import Base

class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer(), primary_key=True)
    slug = Column(String(100), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(100), nullable=False)
    summary = Column(Text, nullable=False)
    year_published = Column(DateTime())
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    slug = Column(String(100), nullable=False, unique=True)
    user_id = Column(Integer())
    review_text = Column(Text, nullable=False)
    rating = Column(Integer(), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    book_id = Column(Integer(), ForeignKey('books.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def get_books():
    return Books.query.all()

if __name__ == "__main__":
    from sqlalchemy.engine import URL

    # url = URL.create(
    #     drivername="postgresql",
    #     username="postgres",
    #     host="/tmp/postgresql/socket",
    #     database="p0$tgr#"
    #)
    url = 'sqlite:///books.db'

    engine = create_engine(url, echo=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    ses = session()
    ses.commit()
    conn = engine.connect()
    conn.execute('show databases')
    pass
