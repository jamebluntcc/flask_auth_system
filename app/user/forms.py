from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.auth.models import User
from flask_login import current_user


class ChangeinfoForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    def __init__(self, *args, **kwargs):
        super(ChangeinfoForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(ChangeinfoForm, self).validate()
        if not initial_validation:
            return False
        if self.username.data != current_user.username:
            self.user = User.query.filter_by(username=self.username.data).first()
            if self.user:
                self.username.errors.append('Username already registered')
                return False
        if self.email.data != current_user.email:
            self.user = User.query.filter_by(email=self.email.data).first()
            if self.user:
                self.email.errors.append('Email already registered')
                return False
        return True


class EditPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password',
                                 validators=[DataRequired()])
    new_password = PasswordField('New Password',
                                 validators=[DataRequired()])
    confirm = PasswordField('Verify Password',
                            validators=[DataRequired(), EqualTo('new_password',
                                                                message='password must match')])

    def __init__(self, *args, **kwargs):
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(EditPasswordForm, self).validate()
        if not initial_validation:
            return False

        if not current_user.check_password(self.old_password.data):
            self.old_password.errors.append('password error')
            return False
        
        if current_user.check_password(self.new_password.data):
            self.new_password.errors.append('new password can not equal old one')
            return False

        return True


