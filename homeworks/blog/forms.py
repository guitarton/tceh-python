from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, validators


class ArticleForm(Form):
    article_title = StringField(label='title', validators=[validators.DataRequired()])
    article_body = TextAreaField(label='body', validators=[validators.DataRequired()])
