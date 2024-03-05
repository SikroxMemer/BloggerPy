from flask import Blueprint , render_template
from app.extenstions import login_manager
from app.models import User

from app import login_required


routes = Blueprint('main', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@routes.route('/')
@login_required
def index():
    return render_template('Home.html')