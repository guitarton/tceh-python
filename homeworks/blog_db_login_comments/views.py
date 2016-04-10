from flask.ext.wtf import Form
from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    flash,
    url_for,
    jsonify,
    escape
)
from flask.ext.login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)

from wtforms.ext.sqlalchemy.orm import model_form

from models import User, Article, Comment
from database import db
from forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__, url_prefix='/auth')
main = Blueprint('main', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', form=RegisterForm())

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('User successfully registered')
        return redirect(url_for('.login'))
    else:
        flash('Incorrect registration!')
        return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', form=LoginForm())

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.user
        login_user(user, remember=True)
        return redirect(url_for('main.index'))
    else:
        flash('Incorrect attempt!')
        return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/', methods=['GET'])
def index():
    articles = Article.query.filter_by(is_visible=True)
    return render_template('articles.html', articles=articles)


@main.route('/new', methods=['GET', 'POST'])
@login_required
def new_article():
    article_form_class = model_form(Article, base_class=Form, db_session=db.session)

    form = article_form_class(request.form)

    if request.method == 'POST' and form.validate():
        form.data['user'] = current_user
        article = Article(title=form.data['title'], content=form.data['content'], user=current_user)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        form = article_form_class()

    return render_template('new_article.html', form=form)


@main.route('/delete/<int:article_id>', methods=['GET'])
def delete(article_id):
    if current_user.is_authenticated:
        if current_user.id == article_id:
            article = Article.query.filter_by(id=article_id).first()
            article.is_visible = False
            db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/ajax/<int:article_id>', methods=['GET', 'POST'])
def ajax_method(article_id):
    if request.method == "POST":
        req = request.json
        user = current_user if current_user.is_authenticated else None
        article = Article.query.filter_by(id=article_id).first()
        content = escape(req['content'])
        if len(content) > 0:
            comment = Comment(content, article, user)
            db.session.add(comment)
            db.session.commit()

    comments = Comment.query.filter_by(article_id=article_id)
    comments_json = {}
    for comment in comments:
        # TODO: add username support ( guest or user)
        comments_json[comment.id] = {"content": comment.content,
                                     "datetime": str(comment.date_created)}
    return jsonify(comments_json)
