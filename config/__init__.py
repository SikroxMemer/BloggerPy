from flask import Flask
from .views import routes
from .extenstions import db

def createApp(config='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    
    with app.app_context():
        db.init_app(app)
        db.create_all()

    app.register_blueprint(routes)
    return app