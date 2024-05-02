from flask import (
    Blueprint, 
    render_template, 
    redirect, 
    url_for , 
    flash , 
    request
)

from app.controllers import (
    PostController , 
    AuthController , 
    ReplyController ,
    ProfileController ,
    AdminController
)

from app.extenstions import login_manager

from app.models import (
    User, 
    Post,
    Category
)

from app import login_required
from os import path , mkdir



try:
    mkdir(path.join(path.dirname(__file__) , 'static' , 'files'))
except:
    pass

routes = Blueprint('main', __name__ , template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return redirect(url_for('main.login'))
    
@routes.route('/')
@login_required
def index():
    page = request.args.get('page' , 1 , type=int)
    category = request.args.get('category' , 'all' , type=str)

    if category == 'all':
        posts = Post.query.paginate(page=page , per_page=5)
    else:
        posts = Post.query.filter_by(category_id=int(category)).paginate(page=page , per_page=5)



    categories = Category.query.all()
    return render_template('home.html', posts=posts , categories=categories)

@routes.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    return AuthController.logout()

@routes.route('/login', methods=['GET', 'POST'])
def login():
    return AuthController.login()

@routes.route('/register', methods=['GET', 'POST'])
def register():
    return AuthController.register()

@routes.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    return PostController.create()

@routes.route('/post/view/id=<int:id>' , methods=['POST','GET'])
@login_required
def view_post(id):
    return PostController.view(id)

@routes.route('/post/delete/id=<int:id>' , methods=['GET','POST'])
@login_required
def delete_post(id):
   return PostController.destroy(id)

@routes.route('/post/edit/id=<int:id>' , methods=['GET' , 'POST'])
@login_required
def edit_post(id):
    return PostController.edit(id)
   
@routes.route('/post/reply/id=<int:id>' , methods=['GET' , 'POST'])
@login_required
def create_reply(id):
   return ReplyController.create(id)

@routes.route('/post/id=<int:post>/reply/delete/id=<int:id>' , methods=['GET' , 'POST'])
@login_required
def delete_reply(id , post):
    return ReplyController.destroy(id , post)

@routes.route('/profile/view/id=<int:id>'  , methods=['GET' , 'POST'])
@login_required
def view_profile(id):
    return ProfileController.view(id)

@routes.route('/profile/edit' , methods=['GET' , 'POST'])
@login_required
def edit_profile():
    return ProfileController.edit()

@routes.route('/post/id=<int:id>/close' , methods=['GET' , 'POST'])
@login_required
def close_topic(id):
   return PostController.close(id)

@routes.route('/admin' , methods=['GET' , 'POST'])
@login_required
def view_admin():
    return AdminController.view()

@routes.errorhandler(401)
def error(error):
    flash('Authentification is required' , 'danger')
    return redirect(url_for('main.login'))