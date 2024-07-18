from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(dueler_id):
    return Dueler.query.get(dueler_id)


class Dueler(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(50), nullable=True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', username = '', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'Dueler {self.email} has been added to the database'
    
class Monster(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    specialty = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(200), nullable=True)
    power_level = db.Column(db.Integer, nullable=True)
    evolution = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('dueler.token'), nullable = False)

    def __init__(self,name, height, weight,specialty,evolution, user_token, type=None, power_level=None, id = ''):
        self.id = self.set_id()
        self.name = name
        self.height = height
        self.weight = weight
        self.specialty = specialty
        self.type = type
        self.power_level = power_level
        self.evolution = evolution
        self.user_token = user_token


    def __repr__(self):
        return f'The following monster has been added to the Monsterdex: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())

class MonsterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','height','weight', 'specialty', 'type', 'power_level', 'evolution']

monster_schema = MonsterSchema()
monsters_schema = MonsterSchema(many=True)