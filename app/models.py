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
    db.Column("GenreId", db.Integer, ForeignKey("genres.id")),
    db.Column("BookId", db.Integer, ForeignKey("books.id")))

class OrderPbooks(db.Model):
    __tablename__ = 'OrderProviderBooks'
    OrderPId = db.Column(db.Integer, ForeignKey("orderProvider.id"), primary_key=True)
    BookId = db.Column(db.Integer, ForeignKey("books.id"), primary_key=True)
    numberOfBooks = db.Column( db.Integer)
    book = db.relationship("Book", back_populates="providerOrder")
    order = db.relationship("OrderToProvider", back_populates="books")

class OrderCbooks(db.Model):
    __tablename__ = 'OrderCustomerBooks'
    OrderCId = db.Column(db.Integer, ForeignKey("orderCustomer.id"), primary_key=True)
    BookId = db.Column(db.Integer, ForeignKey("books.id"), primary_key=True)
    numberOfBooks = db.Column( db.Integer)
    book = db.relationship("Book", back_populates="customerOrder")
    order = db.relationship("OrderFromCustomer", back_populates="books")

class ProvPrices(db.Model):
    __tablename__ = 'ProviderPrices'
    ProviderId = db.Column(db.Integer, ForeignKey("provider.id"), primary_key=True)
    BookId = db.Column(db.Integer, ForeignKey("books.id"), primary_key=True)
    Price = db.Column(db.Integer)
    book = db.relationship("Book", back_populates="providerPrices")
    prov = db.relationship("Provider", back_populates="books")
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
    book = db.relationship("Book", back_populates="warehouse")
    numberOfBooks = db.Column(db.Integer, default=0)

###############


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    surname = db.Column(db.String(64), index=True, unique=False)
    phone = db.Column(db.String(15), index=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(150), index=True)
    isEmployee = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role(self):
        return self.isEmployee

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    surname = db.Column(db.String(64), index=True, unique=False)
    books = db.relationship("Book", secondary=BookAuthor, back_populates="authors")

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
    books = db.relationship("OrderCbooks", back_populates="order")
    bill = db.relationship("CustomerBill", uselist=False, back_populates="order")

class OrderToProvider(db.Model):
    __tablename__ = "orderProvider"
    id = db.Column(db.Integer, primary_key=True)
    ProviderId = db.Column(db.Integer)
    EmployeeId = db.Column(db.Integer)
    books = db.relationship("OrderPbooks", back_populates="order")
    bill = db.relationship("ProviderBill", uselist=False, back_populates="order")

class Provider(db.Model):
    __tablename__ = "provider"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False)
    phone = db.Column(db.String(15), index=True, unique=True)
    address = db.Column(db.String(100), index=True, unique=False)
    books = db.relationship("ProvPrices", back_populates="prov")

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=False)
    price = db.Column(db.Integer, index=True, unique=False)
    year = db.Column(db.Integer, index=True, unique=False)
    authors = db.relationship("Author", secondary=BookAuthor, back_populates="books")
    genres = db.relationship("Genre", secondary=BookGenre, back_populates="books")
    providerOrder = db.relationship("OrderPbooks", back_populates="book")
    customerOrder = db.relationship("OrderCbooks", back_populates="book")
    providerPrices = db.relationship("ProvPrices", back_populates="book")
    warehouse = db.relationship("Warehouse", uselist=False, back_populates="book")
