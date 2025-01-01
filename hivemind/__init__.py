import os
import sys
from dotenv import load_dotenv
from flask import Flask

from hivemind.config import DevelopmentConfig, ProductionConfig, TestingConfig
from hivemind.core.commands import register_commands
from hivemind.core.extensions import db, socketio, login_manager, avatars
from hivemind.models import *
from hivemind.blueprints.settings import settings_bp
from hivemind.blueprints.hive import hive_bp
from hivemind.blueprints.main import main_bp
from hivemind.blueprints.auth import auth_bp
from flask_uploads import configure_uploads

# Load environment variables
load_dotenv()

WIN = sys.platform.startswith('win')

def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object(config)
    
    print(f'Max file size: {app.config['MAX_CONTENT_LENGTH']}')
    print(f'Avatar location: {app.config['UPLOADED_AVATARS_DEST']}')
    
    if config == ProductionConfig:

        db_file_path = os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))

        if WIN:
            db_file_path = db_file_path.replace('\\', '/')

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_path

    # Bind extensions to app
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    
    configure_uploads(app, (avatars))
    
    assert socketio.server is not None, "SocketIO has not been properly initialized!"
    print("SocketIO successfully bound to app.")

    print(f'DB is: {app.config["SQLALCHEMY_DATABASE_URI"]}')

    # Create db from models if in dev/test
    if config in [DevelopmentConfig, TestingConfig]:
        with app.app_context():
            db.create_all()

    # Import and register blueprints
    app.register_blueprint(settings_bp)
    app.register_blueprint(hive_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)


    # Import events for socketio
    import hivemind.events
    
    register_commands(app)
    
    @app.context_processor
    def inject():
        chatrooms = db.session.execute(db.select(Chatroom)).scalars().all()
        return dict(chatrooms=chatrooms)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalars().first()
    return user