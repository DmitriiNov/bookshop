from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# class Book_Author(db.Model):
#     AuthorId = db.Column(db.Integer, ForeignKey("Author.id"))
#     BookId = db.Column(db.Integer, ForeignKey("Book.id"))
#
# class Book_Genre(db.Model):
#     GenreId = db.Column(db.Integer, ForeignKey("Genre.id"))
#     BookId = db.Column(db.Integer, ForeignKey("Book.id"))

# class OrderProviderBooks(db.Model):
#     BookId = db.Column(db.Integer, ForeignKey("Book.id"))
#     OrderPId = db.Column(db.Integer, ForeignKey("OrderToProvider.id"))
#     numberOfBooks = db.Column(db.Integer)
#
# class OrderCustomerBooks(db.Model):
#     BookId = db.Column(db.Integer, ForeignKey("Book.id"))
#     OrderCId = db.Column(db.Integer, ForeignKey("OrderFromCustomer.id"))
#     numberOfBooks = db.Column(db.Integer)

class ProviderBill(db.model):
    OrderPId = db.Column(db.Integer, ForeignKey("OrderToProvider.id"), unique=True,)
    sum = db.Column(db.Integer)

class CustomerBill(db.model):
    OrderCId = db.Column(db.Integer, ForeignKey("OrderFromCustomer.id"), unique=True)
    sum = db.Column(db.Integer)

# class ProviderPrices(db.Model):
#     ProviderId = db.Column(db.Integer, ForeignKey("Provider.id"))
#     BookId = db.Column(db.Integer, ForeignKey("Book.id"))
#     price = db.Column(db.Integer)

class Warehouse(db.Model):
    BookId = db.Column(db.Integer, ForeignKey("Book.id"), unique=True)
    numberOfBooks = db.Column(db.Integer)
