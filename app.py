from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime
from sqlalchemy import or_
import os

app = Flask(__name__, instance_path=os.path.abspath('data'))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///library.sqlite"
app.static_folder = 'static'


@app.route("/")
def book_list():
    sort_by = request.args.get("sort_by", "title")
    search_query = request.args.get("search", "")

    if sort_by == "author":
        sort_column = Author.author_name
    else:
        sort_column = Book.book_title

    search_filter = or_(
        Book.book_title.ilike(f"%{search_query}%"),
        Author.author_name.ilike(f"%{search_query}%")
    )
    books_and_authors = (
        db.session.query(Book.book_id, Book.book_title, Author.author_name, Book.book_isbn)
        .join(Author, Book.author_id == Author.author_id)
        .filter(search_filter)
        .order_by(sort_column)
        .all()
    )
    return render_template("home.html", books_and_authors=books_and_authors)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    endpoint for adding an author
    :return: HTML form to add author
    """
    if request.method == "POST":
        author_name = request.form["name"]
        author_birth_date_str = request.form["birthdate"]
        author_date_of_death_str = request.form["date_of_death"]

        author_birth_date = datetime.strptime(author_birth_date_str, "%Y-%m-%d")
        author_date_of_death = datetime.strptime(author_date_of_death_str, "%Y-%m-%d") \
                               if author_date_of_death_str else None

        new_author = Author(author_name=author_name,
                            author_birth_date=author_birth_date,
                            author_date_of_death=author_date_of_death)

        db.session.add(new_author)
        db.session.commit()

        return f"Author {new_author.author_name}  was successfully added!"

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    endpoint for adding a book
    :return: HTML form to add book
    """
    if request.method == "POST":
        book_isbn = request.form["isbn"]
        book_title = request.form["title"]
        publication_year = request.form["year"]
        author_id = request.form["author_id"]

        new_book = Book(
            book_isbn=book_isbn,
            book_title=book_title,
            publication_year=publication_year,
            author_id=author_id
            )
        db.session.add(new_book)
        db.session.commit()

        return f"Book {new_book.book_title} was successfully added!"

    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book_to_delete = Book.query.get(book_id)

    if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect("/")
    else:
        return f"Book wasn't found"




db.init_app(app)

"""
with app.app_context():
    db.create_all()
"""

if __name__ == '__main__':
    app.run(debug=True)

