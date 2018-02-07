# coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import flash
from settings import Config


def flash_errors(form, category='warning'):
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def output_users(users, filename='WheatAllUsers'):
    output_col = ['realname', 'unit', 'email', 'phone', 'is_pay']
    if not os.path.exists(Config.OUTPUT_FOLDER):
        os.mkdir(Config.OUTPUT_FOLDER)
    filepath = os.path.join(Config.OUTPUT_FOLDER, filename + '.csv')
    filename = filename + '.csv'
    with open(filepath, 'w+') as f:
        f.write(','.join([u'姓名', u'所在单位', u'电子邮件', u'手机号码', u'是否支付']).encode('utf-8') + '\n')
        for user in users:
            each_row = []
            for col in output_col:
                value = str(getattr(user, col))
                each_row.append(value)
            f.write(','.join(each_row) + '\n')

    return filename


