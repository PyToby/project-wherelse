from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(256), nullable=True)
    auth_provider = db.Column(db.String(50), default='email')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_id(self):           # tell Flask-Login to use user_id
        return str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False  # Google user, no password
        return check_password_hash(self.password_hash, password)
    
class Comparison(db.Model):
    comparison_id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(200), unique=True, nullable=False)
    result_json = db.Column(db.Text, nullable=False)
    is_premade = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserHistory(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comparison_id = db.Column(db.Integer, db.ForeignKey('comparison.comparison_id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)