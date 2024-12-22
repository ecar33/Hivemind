import os
import sys
from dotenv import load_dotenv
from flask import Flask

from hivemind.config import DevelopmentConfig, ProductionConfig, TestingConfig
from hivemind.core.commands import register_commands
from hivemind.core.extensions import db
from hivemind.models import *
from hivemind.blueprints.main import main_bp
from hivemind.blueprints.hive import hive_bp

# Load environment variables
load_dotenv()

WIN = sys.platform.startswith('win')

def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object(config)
    
    if config == ProductionConfig:

        db_file_path = os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))

        if WIN:
            db_file_path = db_file_path.replace('\\', '/')

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_path

    # Bind extensions to app
    db.init_app(app)

    print(f'DB is: {app.config["SQLALCHEMY_DATABASE_URI"]}')

    # Create db from models if in dev/test
    if config in [DevelopmentConfig, TestingConfig]:
        with app.app_context():
            db.create_all()

    # Import and register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(hive_bp)

    register_commands(app)

    # @app.context_processor
    # def utility_processor():
    #     pass
    
    return app