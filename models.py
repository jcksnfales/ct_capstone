from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow 
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

# utility methods for creating unique ids
def set_id():
    return str(uuid.uuid4())

def set_token(length):
    return secrets.token_hex(length)

# user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# user model
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    token = db.Column(db.String, default='', unique=True )
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    public_link_count = db.Column(db.Integer, default=0)

    def __init__(self, email, first_name='', last_name='', password=''):
        self.id = set_id()
        self.token = set_token(24)
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.public_link_count = 0
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'{self.email} - {self.public_link_count} public link(s)'

# link listing model
class LinkListing(db.Model):
    listing_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    listed_link = db.Column(db.String, nullable=False)
    link_title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, default='')
    is_public = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, listed_link, link_title, description='', is_public=False):
        self.listing_id = set_id()
        self.user_id = user_id
        self.listed_link = listed_link
        self.link_title = link_title
        self.description = description
        self.is_public = is_public

    def __repr__(self):
        return f'{self.listed_link} - {self.link_title}: {self.description}'
    
class LinkSchema(ma.Schema):
    class Meta:
        fields = ['listing_id', 'user_id', 'listed_link', 'link_title', 'description', 'is_public']

link_schema = LinkSchema()
links_schema = LinkSchema(many=True)