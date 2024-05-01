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
    ProfileController
)

from app.extenstions import login_manager
from app.models import User, Post
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
    posts = Post.query.paginate(page=page , per_page=5)
    return render_template('Home.html', posts=posts)

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
   return PostController.destory(id)

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
    return ReplyController.destory(id , post)

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



# @routes.route("/admin" , methods=['POST' , 'GET'])
# @login_required
# def admin():

#     category_form = CategoryForm()

#     category_page = request.args.get('category_page' , 1 , type=int)
#     user_page = request.args.get('user_page' , 1 , type=int)
#     post_page = request.args.get('post_page' , 1 , type=int)
#     reply_page = request.args.get('reply_page' , 1 , type=int)

#     users = User.query.paginate(page=user_page , per_page=5)
#     posts  = Post.query.paginate(page=post_page , per_page=5)
#     replies = Comment.query.paginate(page=reply_page , per_page=5)
#     categories = Category.query.paginate(page=category_page , per_page=5)


#     if category_form.validate_on_submit():
#         category = Category()
#         category.title = category_form.title.data
#         db.session.add(category)
#         db.session.commit()
#         return redirect(url_for('main.admin'))

#     return render_template(
#         'Admin.html' , 
#         users=users , 
#         posts=posts , 
#         categories=categories , 
#         replies=replies,
#         category_form=category_form
#     )


# @routes.route('/category/delete/id=<int:id>' , methods=['POST' , 'GET'])
# def category_delete(id):
#     category = Category.query.filter_by(id=id).first()
#     db.session.delete(category)
#     db.session.commit()
#     return redirect(url_for('main.admin'))


# @routes.route('/user/delete/id=<int:id>' , methods=['POST' , 'GET'])
# def user_delete(id):
#     user = User.query.filter_by(id=id).first()
#     db.session.delete(user)
#     db.session.commit()
#     return redirect(url_for('main.admin'))

# @routes.route('/comment/delete/id=<int:id>' , methods=['POST' , 'GET'])
# def sudo_reply_delete(id):
#     reply = Comment.query.filter_by(id=id).first()
#     db.session.delete(reply)
#     db.session.commit()
#     return redirect(url_for('main.admin'))






@routes.errorhandler(401)
def error(error):
    flash('Authentification is required' , 'danger')
    return redirect(url_for('main.login'))