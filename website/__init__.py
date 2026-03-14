from flask import Flask
import os


def create_app(): 
    app = Flask(__name__, template_folder='templates')

    from .views import view
    app.register_blueprint(view, url_prefix='/')

    return app