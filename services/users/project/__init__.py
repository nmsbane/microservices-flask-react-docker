# services/users/project/__init__.py
import os

from flask import Flask, jsonify
#from .config import DevelopmentConfig

# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

#app.config.from_object(DevelopmentConfig)

@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
