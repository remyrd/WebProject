from flask.ext.wtf import Form
from wtforms import StringField, SubmitField


class SearchForm(Form):
    search = StringField('Looking for someone?')
    submit = SubmitField('Search')