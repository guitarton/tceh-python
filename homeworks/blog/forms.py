from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, validators


class ArticleForm(Form):
    article_title = StringField('title', [validators.Length(min=3, max=200)])
    article_body = TextAreaField('body', [validators.Length(min=3, max=400)])
