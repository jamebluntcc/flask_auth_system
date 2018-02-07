# coding:utf-8
from flask import redirect, url_for, send_from_directory
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from app.auth.models import User
import flask_login as login
from app.utils import output_users
from settings import Config

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class myAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return super(myAdminIndexView, self).index()

    @expose('/generate_users/')
    def generate_users(self):
        users = User.query.all()
        filename = output_users(users)
        return redirect(url_for('admin.get_users', filename=filename))

    @expose('/get_users/<filename>')
    def get_users(self, filename):
        return send_from_directory(Config.OUTPUT_FOLDER, filename)





    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('main.home'))


class authModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.home'))
