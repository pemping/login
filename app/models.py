from mongoengine import StringField, IntField, BooleanField
from flask_login import UserMixin
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class User(UserMixin, db.Document):
    meta = {
        'collection': 'users',
        'ordering': ['-create_at'],
        'strict': False,
    }
    email = StringField()
    username = StringField()
    password_hash = StringField(max_length=128)
    role_id = IntField()
    confirmed = BooleanField(default=False)

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


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


class Role(db.Document):
    meta = {
        'collection': 'roles'
    }


