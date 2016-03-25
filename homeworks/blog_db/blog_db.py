from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def hello():
    from models import Article
    article_form_class = model_form(Article, base_class=Form, db_session=db.session)

    form = article_form_class(request.form)

    if request.method == 'POST' and form.validate():
        article = Article(**form.data)
        db.session.add(article)
        db.session.commit()
    else:
        form = article_form_class()

    articles = Article.query.filter_by(is_visible=True)
    return render_template('index.html', form=form, articles=articles)


@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    try:
        id = int(id)
    except ValueError:
        pass
    article = Article.query.filter_by(id=id).first()
    article.is_visible = False
    db.session.commit()
    return redirect(url_for('hello'))


if __name__ == '__main__':
    from models import *

    db.create_all()
    app.run()
