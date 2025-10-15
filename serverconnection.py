import os
from flask import Flask, request 
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'WARNINGNOKEYFOUND') #sets key so its not in hardcoded in the code
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print("Unity client connected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port= 948425)