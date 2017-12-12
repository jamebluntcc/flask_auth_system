from flask import Blueprint, flash, redirect, render_template, request, url_for
from .forms import RegisterForm
from flask_login import login_required, logout_user
from .models import User
from app.exetensions import db
from app.utils import flash_errors


blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('main.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    active=True)
        db.session.add(user)
        db.session.commit()
        flash('Thank you for register. You can now loggin.', 'success')
        return redirect(url_for('main.home'))
    else:
        flash_errors(form)
    return render_template('auth/register.html', form=form)