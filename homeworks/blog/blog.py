from flask import Flask, request, render_template
from forms import ArticleForm
from models import Articles, Storage
import CONFIG

app = Flask(__name__)
app.config.from_object(CONFIG)


@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        storage.load()
    except IOError:
        pass
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        if True:
            article = Articles(form.article_title.data, form.article_body.data)
            storage.articles.append(article)
            storage.dump()
    return render_template('base.html', form=form, storage=storage)


if __name__ == '__main__':
    storage = Storage()
    app.run()
