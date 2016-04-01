from flask import Flask, redirect, url_for
from flask.ext.login import LoginManager
from models import User, Article
from database import db
import config

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def create_app():
    from views import auth, main

    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)

    # Blueprints:
    app.register_blueprint(auth)
    app.register_blueprint(main)

    # Custom modules:
    login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'

    db.init_app(app)
    # Dynamic context:
    with app.app_context():
        db.create_all()
    return app


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))
    # return 'Unauthorized', 401


if __name__ == '__main__':
    app = create_app()
    app.run()

