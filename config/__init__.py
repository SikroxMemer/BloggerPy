from flask import Flask
from .views import routes
from .extenstions import db

def createApp(config='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    db.init_app(app)
    app.register_blueprint(routes)
    return app