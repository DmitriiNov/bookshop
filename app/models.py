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

OrderPBooks = db.Table('OrderProviderBooks',
    db.Column("OrderPId", db.Integer, ForeignKey("orderProvider.id")),
    db.Column("BookId", db.Integer, ForeignKey("books.id")),
    db.Column("numberOfBooks", db.Integer))

OrderCBooks = db.Table('OrderCustomerBooks',
    db.Column("OrderCId", db.Integer, ForeignKey("orderCustomer.id")),
    db.Column("BookId", db.Integer, ForeignKey("books.id")),
    db.Column("numberOfBooks", db.Integer))

ProvPrice = db.Table('ProviderPrices',
    db.Column("ProviderId", db.Integer, ForeignKey("provider.id")),
    db.Column("BookId", db.Integer, ForeignKey("books.id")),
    db.Column("Price", db.Integer))
##one to one##

class ProviderBill(db.Model):
    __tablename__ = 'pbill'
    id = db.Column(db.Integer, primary_key=True)
    OrderPId = db.Column(db.Integer, ForeignKey("orderProvider.id"), unique=True)
    order = db.relationship("OrderToProvider", back_populates="bill")
    sum = db.Column(db.Integer)

class CustomerBill(db.Model):
    __tablename__ = 'cbill'
    id = db.Column(db.Integer, primary_key=True)
    OrderCId = db.Column(db.Integer, ForeignKey("orderCustomer.id"), unique=True)
    order = db.relationship("OrderFromCustomer", back_populates="bill")
    sum = db.Column(db.Integer)

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, ForeignKey("books.id"), unique=True)
    book = db.relationship("OrderFromCustomer", back_populates="bill")
    numberOfBooks = db.Column(db.Integer, default=0)

###############


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    surname = db.Column(db.String(64), index=True, unique=False)
    phone = db.Column(db.String(15), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(150), index=True)
    isEmployee = db.Column(db.Boolean, unique=False, default=0)

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
    providerOrder = db.relationship("OrderToProvider", secondary=OrderPBooks, back_populates="books")
    customerOrder = db.relationship("OrderToCustomer", secondary=OrderCBooks, back_populates="books")
    providerPrices = db.relationship("Provider", secondary=ProvPrice, back_populates="books")
    bill = db.relationship("Warehouse", uselist=False, back_populates="book")


class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    books = db.relationship("Book", secondary=BookGenre, back_populates="genres")

class OrderFromCustomer(db.Model):
    __tablename__ = "orderCustomer"
    id = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.Integer)
    EmployeeId = db.Column(db.Integer)
    books = db.relationship("Book", secondary=OrderCBooks, back_populates="customerOrder")
    bill = db.relationship("CustomerBill", uselist=False, back_populates="order")

class OrderToProvider(db.Model):
    __tablename__ = "orderProvider"
    id = db.Column(db.Integer, primary_key=True)
    ProviderId = db.Column(db.Integer)
    EmployeeId = db.Column(db.Integer)
    books = db.relationship("Book", secondary=OrderPBooks, back_populates="providerOrder")
    bill = db.relationship("ProviderBill", uselist=False, back_populates="order")

class Provider(db.Model):
    __tablename__ = "provider"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False)
    phone = db.Column(db.String(15), index=True, unique=True)
    adress = db.Column(db.String(100), index=True, unique=False)
    books = db.relationship("Book", secondary=ProvPrice, back_populates="providerPrices")
