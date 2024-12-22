from hivemind import create_app
from hivemind.config import DevelopmentConfig, ProductionConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(debug=True)