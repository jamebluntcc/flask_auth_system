'''
test mail
'''
import os
from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jamebluntxy@gmail.com'
app.config['MAIL_PASSWORD'] = '87832369et'

mail = Mail(app)

if __name__ == '__main__':
    msg = Message('test mail', sender='jamebluntxy@gmail.com', recipients=['18583994795@163.com'])
    msg.body = 'haha body'
    msg.html = '<b>HTML</b> body'
    with app.app_context():
        mail.send(msg)
