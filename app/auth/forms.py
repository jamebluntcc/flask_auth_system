from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from .models import User


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm = PasswordField('Verify Password',
                            validators=[DataRequired(), EqualTo('password',
                                                                message='password must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        self.user = User.query.filter_by(username=self.username.data).first()
        if self.user:
            self.username.errors.append('Username already registered')
            return False
        self.user = User.query.filter_by(email=self.email.data).first()
        if self.user:
            self.email.errors.append('Email already registered')
            return False
        return True


class LoginForm(FlaskForm):
    username = StringField('Username/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.user = User.query.filter_by(email=self.username.data).first()
            if not self.user:
                self.username.errors.append('Unknow username/email')
                return False
        if not self.user.check_password(self.password.data):
            self.password.errors.append('password error')
            return False
        '''
        if not self.user.active:
            self.username.errors.append('user not active')
            return False
        '''
        return True
