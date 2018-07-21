# services/users/project/__init__.py
import os
import pdb

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar	import DebugToolbarExtension
from flask_cors import CORS
#from .config import DevelopmentConfig

#app.config.from_object(DevelopmentConfig)

# instantiate the db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()

def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    #enable CORS
    CORS(app)

    # set config
    if script_info and type(script_info) == 'str':
        app.config.from_object(script_info)
    else:
        app_settings = os.getenv('APP_SETTINGS')
        app.config.from_object(app_settings)

    # register blueprints
    from api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)

    # create database tables if not already created
    db.app = app
    db.create_all()

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
