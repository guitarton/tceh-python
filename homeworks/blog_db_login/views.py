from flask.ext.wtf import Form
from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    flash,
    url_for,
)
from flask.ext.login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)

from wtforms.ext.sqlalchemy.orm import model_form

from models import User, Article
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


@auth.route('/profile')
@login_required
def view():
    return 'Only logged-in user can see me! Current: {}'.format(
        current_user.username)


@main.route('/', methods=['GET'])
def index():
    # from models import Article
    print(current_user, current_user.is_anonymous)
    articles = Article.query.filter_by(is_visible=True)
    return render_template('articles.html', articles=articles)


@main.route('/new', methods=['GET', 'POST'])
@login_required
def new_article():
    article_form_class = model_form(Article, base_class=Form, db_session=db.session)

    form = article_form_class(request.form)

    if request.method == 'POST' and form.validate():
        form.data['user'] = current_user
        # print(form, form.data, form.user)
        article = Article(title=form.data['title'], content=form.data['content'], user=current_user)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        form = article_form_class()

    print(current_user.username)
    return render_template('new_article.html', form=form)


@main.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    print(current_user.id, current_user.username)
    if current_user.id == id:
        article = Article.query.filter_by(id=id).first()
        article.is_visible = False
        db.session.commit()
    return redirect(url_for('main.index'))
