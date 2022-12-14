# -*- coding:utf-8 -*-

from flask import Flask
from flask_socketio import SocketIO
from config import DevConfig
from flask_cors import CORS
from flask_bootstrap import Bootstrap

socketio = SocketIO()
bootstrap = Bootstrap()

def create_app(config):
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    
    CORS(app)

    from .User_Access import user_access
    app.register_blueprint(user_access)

    socketio.init_app(app)
    bootstrap.init_app(app)
    return app




