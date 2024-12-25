from hivemind import create_app
from hivemind.config import DevelopmentConfig
from hivemind.core.extensions import socketio

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    socketio.run(app, debug=True)