from flask_website import app, socketio

import os

if __name__ == '__main__':
    print("getcwd():", os.getcwd())
    socketio.run(app)
