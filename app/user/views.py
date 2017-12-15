from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import ChangeinfoForm, EditPasswordForm
from app.mail import send_mail
from app.utils import flash_errors
blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/members/')
@login_required
def members():
    return render_template('user/members.html')


@blueprint.route('/update/')
@login_required
def update():
    info_form = ChangeinfoForm()
    passwd_form = EditPasswordForm()
    return render_template('user/update.html', info_form=info_form, passwd_form=passwd_form)


@blueprint.route('/change_passwd/', methods=['POST'])
@login_required
def change_passwd():
    passwd_form = EditPasswordForm()
    info_form = ChangeinfoForm()
    if passwd_form.validate_on_submit():
        current_user.set_password(passwd_form.new_password.data)
        current_user.save()
        flash('hi {}, Already update your password.'.format(current_user.username), 'success')
        return redirect(url_for('users.members'))
    else:
        flash_errors(passwd_form)
        return render_template('user/update.html', info_form=info_form, passwd_form=passwd_form)


@blueprint.route('/change_info/', methods=['GET', 'POST'])
@login_required
def change_info():
    info_form = ChangeinfoForm()
    passwd_form = EditPasswordForm()
    if request.method == 'POST':
        if info_form.validate_on_submit():
            old_email = current_user.email
            current_user.update(username=info_form.username.data,
                                email=info_form.email.data)
            if info_form.email.data != old_email:
                token = current_user.generate_confirmation_token()
                send_mail(info_form.email.data, 'Confirm Your Account',
                          'auth/confirm', user=current_user, token=token)
                flash('Seems you change your email. A confirmation email has been sent to you by email. \
                        note: open verify email better on your pc browser', 'success')
            flash('hi {}, Already update your infomation.'.format(info_form.username.data), 'success')
            return redirect(url_for('users.members'))
        else:
            flash_errors(info_form)
            return render_template('user/update.html', info_form=info_form, passwd_form=passwd_form)




