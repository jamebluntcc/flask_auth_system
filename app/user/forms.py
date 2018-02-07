# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.auth.models import User
from flask_login import current_user


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SummaryForm(FlaskForm):
    title = StringField(u'标题',
                        validators=[DataRequired()])
    author = StringField(u'作者',
                         validators=[DataRequired()])
    unit = StringField(u'所属单位',
                       validators=[DataRequired()])
    kwords = StringField(u'关键词',
                         validators=[DataRequired()])
    text = TextAreaField(u'摘要',
                         validators=[DataRequired()])


class PayForm(FlaskForm):
    pay_online = MultiCheckboxField(u'支付方式',
                                    choices=[('y', u'现在支付'), ('n', u'线下支付')])


class ChangeinfoForm(FlaskForm):
    username = StringField(u'用户名',
                           validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField(u'邮箱',
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
                self.username.errors.append(u'用户名已经被使用')
                return False
        if self.email.data != current_user.email:
            self.user = User.query.filter_by(email=self.email.data).first()
            if self.user:
                self.email.errors.append(u'邮箱已经被注册')
                return False
        return True


class EditPasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码',
                                 validators=[DataRequired()])
    new_password = PasswordField(u'新密码',
                                 validators=[DataRequired()])
    confirm = PasswordField(u'确认密码',
                            validators=[DataRequired(), EqualTo('new_password',
                                                                message=u'密码不一致')])

    def __init__(self, *args, **kwargs):
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(EditPasswordForm, self).validate()
        if not initial_validation:
            return False

        if not current_user.check_password(self.old_password.data):
            self.old_password.errors.append(u'密码无效')
            return False
        
        if current_user.check_password(self.new_password.data):
            self.new_password.errors.append(u'密码不一致')
            return False

        return True


