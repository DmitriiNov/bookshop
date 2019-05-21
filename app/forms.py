from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms.fields.html5 import TelField
import phonenumbers

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone number (+7)', validators=[DataRequired()])

    submit = SubmitField('Register')


    # def validate_phone(form, field):
    #     user = User.query.filter_by(phone = field).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different phone number.')
    #     if len(field.data) > 12:
    #         raise ValidationError('Invalid phone number.')
    #     try:
    #         input_number = phonenumbers.parse(field.data)
    #         if not (phonenumbers.is_valid_number(input_number)):
    #             raise ValidationError('Invalid phone number.')
    #     except:
    #         input_number = phonenumbers.parse("+7"+field.data)
    #         if not (phonenumbers.is_valid_number(input_number)):
    #             raise ValidationError('Invalid phone number.')
