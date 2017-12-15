from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user
from .forms import ChangeinfoForm
from app.mail import send_mail
from app.utils import flash_errors
blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/members/')
@login_required
def members():
    return render_template('user/members.html')


@blueprint.route('/change_info/', methods=['GET', 'POST'])
@login_required
def change_info():
    form = ChangeinfoForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            old_email = current_user.email
            current_user.update(username=form.username.data,
                                email=form.email.data,
                                passeword=form.new_password.data)
            if form.email.data != old_email:
                token = current_user.generate_confirmation_token()
                send_mail(form.email.data, 'Confirm Your Account',
                          'auth/confirm', user=current_user, token=token)
                flash('Seems you change your email. A confirmation email has been sent to you by email. \
                        note: open verify email better on your pc browser', 'success')
            flash('hi {}, Already update your infomation.'.format(form.username.data), 'success')
            return redirect(url_for('users.members'))
        else:
            flash_errors(form)
    return render_template('user/update.html', form=form)




