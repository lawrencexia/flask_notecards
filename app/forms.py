from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class NoteForm(Form):
    title = StringField('title')
    message = TextAreaField('message', validators=[DataRequired()])