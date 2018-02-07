# coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, Blueprint, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from .forms import ChangeinfoForm, EditPasswordForm, SummaryForm, PayForm
from app.mail import send_mail
from app.utils import flash_errors, allowed_file
from app.auth.models import Summary
from werkzeug.utils import secure_filename
from settings import Config

blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/members/')
@login_required
def members():
    if current_user.summary_id:
        current_summary = current_user.summary
    else:
        current_summary = None
    return render_template('user/members.html',
                           current_summary=current_summary)


@blueprint.route('/summary/', methods=['GET', 'POST'])
@login_required
def summary():
    pay_form = PayForm()
    summary_form = SummaryForm()
    info_form = ChangeinfoForm()
    passwd_form = EditPasswordForm()
    if summary_form.validate_on_submit():
        current_summary = Summary(title=summary_form.title.data,
                                  author=summary_form.author.data,
                                  kwords=summary_form.kwords.data,
                                  unit=summary_form.unit.data,
                                  text=summary_form.text.data)
        current_summary.save()
        current_user.update(summary_id=current_summary.id)
        flash(u'hi {}, 已经更新摘要.'.format(current_user.username), 'success')
        return redirect(url_for('users.members'))
    flash_errors(summary_form)
    return render_template('user/update.html',
                           summary_form=summary_form,
                           pay_form=pay_form,
                           info_form=info_form,
                           passwd_form=passwd_form)


@blueprint.route('/pay_method/', methods=['GET', 'POST'])
@login_required
def pay_method():
    pay_form = PayForm()
    summary_form = SummaryForm()
    info_form = ChangeinfoForm()
    passwd_form = EditPasswordForm()
    if pay_form.validate_on_submit():
        if pay_form.pay_online.data[0] == 'y':
            current_user.update(is_online_pay=True)
        else:
            current_user.update(is_online_pay=False)
        flash(u'hi {}, 已经更新支付方式.'.format(current_user.username), 'success')
        return redirect(url_for('users.members'))
    flash_errors(pay_form)
    return render_template('user/update.html',
                           summary_form=summary_form,
                           pay_form=pay_form,
                           info_form=info_form,
                           passwd_form=passwd_form)


@blueprint.route('/update/', methods=['GET'])
@login_required
def update():
    info_form = ChangeinfoForm()
    passwd_form = EditPasswordForm()
    summary_form = SummaryForm()
    pay_form = PayForm()
    return render_template('user/update.html',
                           info_form=info_form,
                           passwd_form=passwd_form,
                           summary_form=summary_form,
                           pay_form=pay_form)


@blueprint.route('/change_passwd/', methods=['POST'])
@login_required
def change_passwd():
    passwd_form = EditPasswordForm()
    info_form = ChangeinfoForm()
    if passwd_form.validate_on_submit():
        current_user.set_password(passwd_form.new_password.data)
        current_user.save()
        flash('hi {}, 已经更新密码.'.format(current_user.username), 'success')
        return redirect(url_for('users.members'))
    else:
        flash_errors(passwd_form)
        return render_template('user/update.html', info_form=info_form, passwd_form=passwd_form)


@blueprint.route('/change_info/', methods=['GET', 'POST'])
@login_required
def change_info():
    info_form = ChangeinfoForm()
    passwd_form = EditPasswordForm()
    summary_form = SummaryForm()
    pay_form = PayForm()
    if request.method == 'POST':
        if info_form.validate_on_submit():
            old_email = current_user.email
            current_user.update(username=info_form.username.data,
                                email=info_form.email.data,
                                phone=info_form.phone.data,
                                unit=info_form.unit.data)
            if info_form.email.data != old_email:
                token = current_user.generate_confirmation_token()
                send_mail(info_form.email.data, 'Confirm Your Account',
                          'auth/confirm', user=current_user, token=token)
                flash(u'似乎您已经改变邮箱地址,一封新的确认邮件已经发送到您的新邮箱地址请注意查收.', 'success')
            flash('hi {}, 已经更新邮箱地址.'.format(info_form.username.data), 'success')
            return redirect(url_for('users.members'))
        flash_errors(info_form)

    return render_template('user/update.html',
                           info_form=info_form,
                           passwd_form=passwd_form,
                           summary_form=summary_form,
                           pay_form=pay_form)


@blueprint.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload_summary():
    info_form = ChangeinfoForm()
    passwd_form = EditPasswordForm()
    summary_form = SummaryForm()
    pay_form = PayForm()
    if request.method == 'POST':
        if 'summary' not in request.files or request.files['summary'].filename == '':
            flash(u'当前没有选取到您上传的摘要', 'danger')
            return redirect(url_for('users.update'))
        file = request.files['summary']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            saveFilename = '_'.join([current_user.username, filename])
            current_user.update(filename=saveFilename)
            file.save(os.path.join(Config.UPLOAD_FOLDER, saveFilename))
            flash(u'摘要上传成功', 'success')
            redirect(url_for('users.members'))
        else:
            flash(u'上传文件格式不正确', 'danger')
            redirect(url_for('users.update'))
    return render_template('user/update.html',
                           info_form=info_form,
                           passwd_form=passwd_form,
                           summary_form=summary_form,
                           pay_form=pay_form)


@blueprint.route('/upload/<filename>')
@login_required
def uploadfile(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)










