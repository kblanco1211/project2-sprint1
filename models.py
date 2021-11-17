from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from opensea import get_assets, get_single_asset
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
 
login = LoginManager()
db = SQLAlchemy()

class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
class NFTsave(db.Model):
    __tablename__= 'nfts'
    id = db.Column(db.Integer, primary_key=True)
    contract_address = db.Column(db.String(200), nullable=False)
    token_id = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100))


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))