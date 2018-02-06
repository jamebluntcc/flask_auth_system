# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from .models import User


class RegisterForm(FlaskForm):
    username = StringField(u'用户名',
                           validators=[DataRequired(), Length(min=2, max=30)])
    realname = StringField(u'真实姓名',
                           validators=[DataRequired(), Length(min=2, max=30)])
    unit = StringField(u'所在单位',
                       validators=[DataRequired()])
    phone = StringField(u'手机号码',
                        validators=[DataRequired(), Regexp("1[34578][0-9]{9}", message=u'手机号码格式不正确')])
    email = StringField(u'邮箱',
                        validators=[DataRequired(), Email()])
    password = PasswordField(u'密码',
                             validators=[DataRequired()])
    confirm = PasswordField(u'确认密码',
                            validators=[DataRequired(), EqualTo('password',
                                                                message=u'密码不一致')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        self.user = User.query.filter_by(username=self.username.data).first()
        if self.user:
            self.username.errors.append(u'用户已经注册')
            return False
        self.user = User.query.filter_by(email=self.email.data).first()
        if self.user:
            self.email.errors.append(u'邮箱已经注册')
            return False
        self.user = User.query.filter_by(phone=self.phone.data).first()
        if self.user:
            self.phone.errors.append(u'电话已经注册')
            return False
        return True


class LoginForm(FlaskForm):
    username = StringField(u'用户名/邮箱', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])

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
                self.username.errors.append(u'无效用户名/邮箱')
                return False
        if not self.user.check_password(self.password.data):
            self.password.errors.append(u'密码无效')
            return False
        '''
        if not self.user.active:
            self.username.errors.append('user not active')
            return False
        '''
        return True
