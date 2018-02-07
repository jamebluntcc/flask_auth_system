# coding:utf-8
from app.exetensions import bcrypt, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
import datetime


class CRUDMixin(object):
    """ base model """
    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class User(UserMixin, CRUDMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    realname = db.Column(db.String(80), nullable=False)
    unit = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=False)
    is_pay = db.Column(db.Boolean(), default=False)
    is_online_pay = db.Column(db.Boolean(), default=False)
    summary_id = db.Column(db.Integer, db.ForeignKey('summary.id'))
    filename = db.Column(db.String(80), nullable=True)

    def __init__(self, username, realname, unit, email, phone, active, is_pay=False, filename=None, password=None, is_admin=False, summary_id=None, is_online_pay=False):
        self.username = username
        self.realname = realname
        self.unit = unit
        self.phone = phone
        self.email = email
        self.active = active
        self.is_pay = is_pay
        self.filename = filename
        self.is_admin = is_admin
        self.is_online_pay = is_online_pay
        self.summary_id = summary_id
        self.create_at = datetime.datetime.now()
        if password:
            self.set_password(password)
        else:
            self.password = None

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    @classmethod
    def confirm(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None

        user = cls.query.filter_by(id=data.get('confirm')).first()
        return user

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        return '<user:{0}>'.format(self.username)


class Summary(CRUDMixin, db.Model):
    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    unit = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    kwords = db.Column(db.String(80), nullable=False)
    users = db.relationship('User', backref='summary', lazy=True)

    def __init__(self, title, author, unit, text, kwords):
        self.title = title
        self.author = author
        self.unit = unit
        self.text = text
        self.kwords = kwords

    def __repr__(self):
        return '<summary: {0}>'.format(self.title)

