from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, IntegerField,BooleanField,SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp,Optional




class ContactForm(FlaskForm):
    firstname = StringField('First Name', render_kw={'placeholder':'First Name'}, validators=[DataRequired(), Length(1,100)])
    lastname = StringField('Last Name', render_kw={'placeholder':'Last Name'}, validators=[DataRequired(), Length(1,100)])
    email = StringField('Email Address', render_kw={'placeholder':'Email'}, validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', render_kw={'placeholder':'+234 80 0000 0000'}, validators=[DataRequired(),
                                                        Regexp(r'(^[0]\d{10}$)|(^[\+]?[234]\d{12}$)',0, 'Enter a valid Phone Number e.g +234801234**** ')])                  
    message = TextAreaField('Message', render_kw={'placeholder':'Message'}, validators = [DataRequired()])
    submit = SubmitField('Submit')
