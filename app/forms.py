from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Provider
from wtforms.fields.html5 import TelField
import phonenumbers



class BookSearch(FlaskForm):
    authors= SelectMultipleField('Authors', coerce=int)
    genres= SelectMultipleField('Genres', coerce=int)
    submit= SubmitField('Search')

class AddBook(FlaskForm):
    name= StringField('Name', validators=[DataRequired()])
    price= StringField('Price', validators=[DataRequired()])
    year= StringField('Year', validators=[DataRequired()])
    authors= SelectMultipleField('Authors', coerce=int, validators=[DataRequired()])
    genres= SelectMultipleField('Genres', coerce=int, validators=[DataRequired()])
    submit1= SubmitField('Add book')

class AddProvPrice(FlaskForm):
    provider= SelectField('Providers', coerce=int, validators=[DataRequired()])
    book= SelectField('Books', coerce=int, validators=[DataRequired()])
    price= StringField('Price', validators=[DataRequired()])
    submit6= SubmitField('Add Price')

class MakePOrder(FlaskForm):
    provider= SelectField('Choose Provider', coerce=int, validators=[DataRequired()])
    submit7= SubmitField('Make')

class AddGenre(FlaskForm):
    name= StringField('Name', validators=[DataRequired()])
    submit2= SubmitField('Add genre')

class AddAuthor(FlaskForm):
    name= StringField('Name', validators=[DataRequired()])
    surname= StringField('Surname', validators=[DataRequired()])
    submit3= SubmitField('Add author')

class AddProvider(FlaskForm):
    name= StringField('Name', validators=[DataRequired()])
    address= StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit4 = SubmitField('Add provider')

class Delete(FlaskForm):
    table= SelectField('Table', coerce=int,choices=[(1,'Book'),(2,'Genre'),(3,'Author'),(4,'Provider')], validators=[DataRequired()])
    id= StringField('ID', validators=[DataRequired()])
    submit5 = SubmitField('Delete')

class OrderUser(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class OrderProvider(FlaskForm):
    providerId = StringField('Provider ID', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    def validate_providerId(form, field):
        a = User.query.filter_by(phone = field.data).first()
        if a is not None:
            raise ValidationError('Please use a different phone number.')
        if len(str(field)) != 10:
            raise ValidationError('Invalid phone number.')

class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone number (without +7)', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_phone(form, field):
        a = User.query.filter_by(phone = field.data).first()
        if a is not None:
            raise ValidationError('Please use a different phone number.')
        if len(str(field.data)) != 10:
            raise ValidationError('Invalid phone number.')
