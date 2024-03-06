from flask_login import login_required


from flask import Flask
from app.extenstions import db, login_manager, bcrypt
from app.views import routes


def create(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    with app.app_context():
        db.init_app(app)
        login_manager.init_app(app)
        bcrypt.init_app(app)
        db.create_all()

    app.register_blueprint(routes)

    return app
