from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms.fields.html5 import TelField
import phonenumbers





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
    phone = StringField('Phone number ( without +7)', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_phone(form, field):
        a = User.query.filter_by(phone = field.data).first()
        if a is not None:
            raise ValidationError('Please use a different phone number.')
        if len(field) == 10:
            raise ValidationError('Invalid phone number.')
