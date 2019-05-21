from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import  ForeignKey

##Отношения##
##many to many##
BookAuthor = db.Table('book_author',
    db.Column("AuthorId", db.Integer, ForeignKey("authors.id")),
    db.Column("BookId", db.Integer, ForeignKey("books.id")))

BookGenre = db.Table('book_genre',
    db.Column("GenreId", db.Integer, ForeignKey("authors.id")),
    db.Column("BookId", db.Integer, ForeignKey("books.id")))



class OrderProviderBooks(db.Model):
    BookId = db.Column(db.Integer, ForeignKey("Book.id"))
    OrderPId = db.Column(db.Integer, ForeignKey("OrderToProvider.id"))
    numberOfBooks = db.Column(db.Integer)

class OrderCustomerBooks(db.Model):
    BookId = db.Column(db.Integer, ForeignKey("Book.id"))
    OrderCId = db.Column(db.Integer, ForeignKey("OrderFromCustomer.id"))
    numberOfBooks = db.Column(db.Integer)

class ProviderPrices(db.Model):
    ProviderId = db.Column(db.Integer, ForeignKey("Provider.id"))
    BookId = db.Column(db.Integer, ForeignKey("Book.id"))
    price = db.Column(db.Integer)

###############


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    surname = db.Column(db.String(64), index=True, unique=False)
    phone = db.Column(db.String(15), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(150), index=True)
    isEmployee = db.Column(db.Boolean, unique=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    surname = db.Column(db.String(64), index=True, unique=False)
    books = db.relationship("Book", secondary=BookAuthor, back_populates="authors")

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=False)
    price = db.Column(db.Integer, index=True, unique=False)
    year = db.Column(db.Integer, index=True, unique=False)
    authors = db.relationship("Author", secondary=BookAuthor, back_populates="books")
    genres = db.relationship("Genre", secondary=BookGenre, back_populates="books")

class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    books = db.relationship("Book", secondary=BookGenre, back_populates="genres")

class OrderFromCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.Integer)
    EmployeeId = db.Column(db.Integer)

class OrderToProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ProviderId = db.Column(db.Integer)
    EmployeeId = db.Column(db.Integer)


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False)
    phone = db.Column(db.String(15), index=True, unique=True)
    adress = db.Column(db.String(100), index=True, unique=False)
