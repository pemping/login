from mongoengine import StringField, IntField, BooleanField, ReferenceField, DateTimeField, ListField
from flask_login import UserMixin
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime


class Role(db.Document):
    meta = {
        'collection': 'roles'
    }
    name = StringField(max_length=64, unique=True)
    default = BooleanField(default=False)
    permissions = IntField()


class User(UserMixin, db.Document):
    meta = {
        'collection': 'users',
        'ordering': ['-create_at'],
        'strict': False,
    }

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     self.role_id = Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES

    email = StringField()
    username = StringField()
    password_hash = StringField(max_length=128)
    role_id = IntField()
    confirmed = BooleanField(default=False)
    about_me = StringField()
    member_since = DateTimeField(default=datetime.utcnow)
    last_seen = DateTimeField(default=datetime.utcnow)
    role = ReferenceField(Role)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': str(self.id)})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != str(self.id):
            return False
        self.confirmed = True
        self.save()
        return True

    def is_admin(self):
        return self.role is not None and (self.role.permissions & Permission.ADMINISTER) == Permission.ADMINISTER


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

