from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')