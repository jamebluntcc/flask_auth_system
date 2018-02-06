# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Blueprint, flash, redirect, render_template, url_for, request
from .forms import RegisterForm
from flask_login import login_required, logout_user, current_user, login_user
from .models import User
from app.utils import flash_errors
from app.mail import send_mail
from settings import Config


blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.active \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@blueprint.route('/unconfirmed/')
def unconfirmed():
    if current_user.is_anonymous or current_user.active:
        return redirect(url_for('main.index'))
    mail_addr = Config.MAIL_MAP.get(current_user.email.split('@')[1], '')
    return render_template('auth/unconfirmed.html', mail=mail_addr)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(u'您已经登出.', 'info')
    return redirect(url_for('main.home'))


@blueprint.route('/confirm/<token>')
def confirm(token):
    user = User.confirm(token)
    if user:
        if user.active:
            flash(u'您已经更新邮箱信息.', 'success')
            login_user(user)
            return redirect(url_for('users.members'))
        if not user.active:
            user.update(active=True)
            flash(u'您已经确认邮箱帐号.', 'success')
    else:
        flash(u'令牌已经失效,请重新发送邮件.', 'danger')
    return redirect(url_for('main.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    realname=form.realname.data,
                    unit=form.unit.data,
                    phone=form.phone.data,
                    email=form.email.data,
                    password=form.password.data,
                    active=False)
        user.save()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm Your Account',
                  'auth/confirm', user=user, token=token)
        flash(u'感谢您的注册,一封确认邮件将会被发送到您的邮箱,请注意查收.', 'success')
        login_user(user)
        return redirect(url_for('main.home'))
    else:
        flash_errors(form)
    return render_template('auth/register.html', form=form)


@blueprint.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Confirm Your Account',
              'auth/confirm', user=current_user, token=token)
    flash(u'一封新的确认邮件已经发送到您的邮箱.', 'success')
    return redirect(url_for('main.home'))
