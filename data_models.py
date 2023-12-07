from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime



db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String, nullable=False)
    author_birth_date = Column(DateTime, nullable=False)
    author_date_of_death = Column(DateTime, nullable=True)

    """
        def __init__(self, author_name, author_birth_date, author_date_of_death): #should I use it?
        self.author_name = author_name
        self.author_birth_date = author_birth_date
        self.author_date_of_death = author_date_of_death
    """

    def __repr__(self):
        return f"Author(author_id = {self.author_id}, name = {self.author_name})"

class Book(db.Model):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(String, unique=True, nullable=False) #should it be a primary key?
    book_title = Column(String)
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)

    def __repr__(self):
        return f"Book(book_id = {self.book_id}, title = {self.book_title})"



