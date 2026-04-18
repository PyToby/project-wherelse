from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, logging
from flask_login import LoginManager
from .models import User, db

login_manager = LoginManager()

def create_app(): 
    logger = logging.getLogger(__name__)
    logger.Formatter(
        "{asctime} - {levelname}: {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )
    
    app = Flask(__name__, template_folder='templates', static_folder='../static')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,  # drops stale connections automatically
        "pool_size": 5,
        "max_overflow": 10,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # redirect here if not logged in

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views import view
    app.register_blueprint(view, url_prefix='/')
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    with app.app_context():
        db.create_all()
    
    return app

