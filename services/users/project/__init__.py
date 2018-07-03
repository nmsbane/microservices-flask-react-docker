# services/users/project/__init__.py

from flask import Flask, jsonify
#from .config import DevelopmentConfig
# instantiate the app
app = Flask(__name__)

# set config
app.config.from_object('project.config.DevelopmentConfig')
#app.config.from_object(DevelopmentConfig)

@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
