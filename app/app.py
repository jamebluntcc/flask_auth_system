from flask import Flask, render_template
from .exetensions import db, bcrypt, login_manager, migrate, mail
from auth.models import User
from admin.views import authModelView, myAdminIndexView
from . import auth, main, user
from settings import config
from flask_admin import Admin
import assets


def create_app(configStr='dev'):
    app = Flask(__name__)
    app.config.from_object(config[configStr])
    register_blueprint(app)
    register_exetensions(app)
    register_errorhandlers(app)
    register_admin(app)
    return app


def register_exetensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    assets.init_app(app)
    return None


def register_blueprint(app):
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(main.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_admin(app):
    admin = Admin(app, index_view=myAdminIndexView(), base_template='admin/nav.html')
    admin.add_view(authModelView(User, db.session))
