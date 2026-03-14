from flask import Flask
import os


def create_app(): 
    app = Flask(__name__)

    from .views import view
    app.register_blueprint(view, url_prefix='/')

    return app