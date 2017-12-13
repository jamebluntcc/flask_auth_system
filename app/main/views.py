from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.auth.forms import LoginForm
from flask_login import login_user, login_required
from app.exetensions import login_manager
from app.utils import flash_errors
from app.auth.models import User
blueprint = Blueprint('main', __name__, url_prefix='/main')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/home/', methods=['GET', 'POST'])
@blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('main.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('home.html', form=form)


@blueprint.route('/user/')
@login_required
def members():
    return render_template('user/members.html')