from flask import Blueprint, flash, redirect, render_template, url_for, request
from .forms import RegisterForm
from flask_login import login_required, logout_user, current_user
from .models import User
from app.utils import flash_errors
from app.mail import send_mail


blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('main.home'))


@blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.active:
        return redirect(url_for('main.home'))
    if current_user.confirm(token):
        flash('you have confirmed your account. Thanks!')
    else:
        flash('the confirmation link is invalid or has expired.')
    return redirect(url_for('main.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    active=False)
        user.save()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm Your Account',
                  'auth/confirm', user=user, token=token)
        flash('Thank you for register. A confirmation email has been sent to you by email.', 'success')
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
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.home'))