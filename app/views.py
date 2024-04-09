from flask import (Blueprint, render_template, redirect, url_for , flash , request)
from app.extenstions import (login_manager, bcrypt, db)
from app.models import (User, Post, Category , Comment)
from app.forms import (LoginForm, ReiterationForm, PostForm , EditForm , ReplyForm , ProfileForm , CategoryForm)
from app.settings import (UPLOAD_FOLDER)
from app import (login_required, logout_user, login_user , current_user)
from os import (path , mkdir)
from werkzeug.utils import (secure_filename)
from datetime import (datetime)
from base64 import (b64encode)

try:
    mkdir(path.join(path.dirname(__file__) , 'static' , 'files'))
except:
    pass

routes = Blueprint('main', __name__, template_folder='templates')

def secureFilename(filename:str):
    __DIR__ = path.join(path.abspath(path.dirname(__file__)) , UPLOAD_FOLDER , secure_filename(filename=filename))
    return __DIR__

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return redirect(url_for('main.login'))
    

@routes.route('/')
def index():
    if current_user.is_authenticated:
        page = request.args.get('page' , 1 , type=int)
        posts = Post.query.paginate(page=page , per_page=5)
        return render_template('Home.html', posts=posts)
    else:
        return redirect(url_for('main.login'))

    


@routes.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash("You've loged out" , "danger")
    return redirect(url_for('main.login'))


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've Successfuly Loged In !" , "success")
                if user.type == 'User':
                    return redirect(url_for('main.index'))
                else:
                    return redirect(url_for('main.admin'))
            else:
                flash("Error : Wrong Credentials , please check your email or password" , "danger")
        else:
            flash("Warning : User Doesn't Exist" , "warning")

    return render_template('Login.html', form=form)


@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = ReiterationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,password=hashed_password, email=form.email.data)
    
        db.session.add(new_user)
        db.session.commit()

        flash("Your account has been created!", "success")
        return redirect(url_for('main.login'))

    return render_template('Register.html', form=form)


@routes.route('/post/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_authenticated:
        categories = Category.query.all()
        choices: list[tuple] = []
        for choice in categories:
            choices.append((choice.id, choice.title))
        form = PostForm()
        form.category.choices = choices
        if form.validate_on_submit():
            post = Post()
            post.title = form.title.data
            post.story = form.story.data
            post.category_id = form.category.data
            post.post_owner = User.query.filter_by(id=current_user.id).first()
            db.session.add(post)
            db.session.commit()

            flash("Your post has been created!", "success")

            return redirect(url_for('main.index'))
        return render_template('Create.html', form=form)
    else:
        return redirect(url_for('main.login'))


@routes.route('/post/view/id=<int:id>' , methods=['POST' , 'GET'])
@login_required
def view(id):
    if current_user.is_authenticated:
        page = request.args.get('page' , 1 , type=int)

        post = Post.query.filter_by(id=id).first()
        replies = Comment.query.filter_by(post=post).paginate(page=page , per_page=5)


        return render_template('Post.html', post=post , replies=replies)
    else:
        return redirect(url_for('main.login'))


@routes.route('/post/delete/id=<int:id>' , methods=['GET' , 'POST'])
@login_required
def post_delete(id):
    if current_user.is_authenticated:
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted', 'warning')
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.login'))


@routes.route('/post/edit/id=<int:id>' , methods=['GET' , 'POST'])
@login_required
def post_edit(id):
    if current_user.is_authenticated:
        categories = Category.query.all()
        choices: list[tuple] = []
        for choice in categories:
            choices.append((choice.id, choice.title))
        post = Post.query.filter_by(id=id).first()
        form = EditForm()
        form.edit_category.choices = choices
        if form.validate_on_submit():
            post.title = form.edit_title.data
            post.story = form.edit_story.data
            post.category_id = form.edit_category.data
            db.session.commit()
            flash('Your post has been edited', 'info')
            return redirect(url_for('main.view', id=id))
            ...
        return render_template('Edit.html', post=post , form=form)
    else:
       return redirect(url_for('main.login'))

@routes.route('/post/reply/id=<int:id>' , methods=['GET' , 'POST'])
@login_required
def reply(id):
    if current_user.is_authenticated:
        form = ReplyForm()
        post = Post.query.filter_by(id=id).first()

        if form.validate_on_submit():
            story = form.story.data
            reply = Comment()

            reply.comment_owner_id = current_user.id
            reply.comment = story
            reply.post = post

            db.session.add(reply)
            db.session.commit()

            flash('Reply Added' , 'success')

            return redirect(url_for('main.view' , id=id))

        return render_template('Reply.html', post=post , form=form)
    else:
        return redirect(url_for('main.login'))


@routes.route('/post/id=<int:post>/reply/delete/id=<int:id>' , methods=['GET' , 'POST'])
@login_required
def reply_delete(id , post):
    if current_user.is_authenticated:
        reply = Comment.query.filter_by(id=id).first()
        db.session.delete(reply)
        db.session.commit()
        flash('Reply Deleted' , 'info')
        return redirect(url_for('main.view' , id=post))
    else:
        return redirect(url_for('main.login'))

@routes.route('/profile/view/id=<int:id>'  , methods=['GET' , 'POST'])
@login_required
def profile(id):
    if current_user.is_authenticated:
        user = User.query.filter_by(id=id).first()
        if not user:
            flash('No User with the ID : {} Found !'.format(id) , 'danger')
            return redirect(url_for('main.index'))
        return render_template('Profile.html' , user=user)
    else:
        return redirect(url_for('main.login'))


@routes.route('/profile/edit' , methods=['GET' , 'POST'])
@login_required
def profile_edit():
    if current_user.is_authenticated:
        form = ProfileForm()
        user = User.query.filter_by(id=current_user.id).first()
        if form.validate_on_submit():
            file = form.profile_picture.data
            try:

                if file.filename:
                    file.save(secureFilename(file.filename))
                    user.profile_picture = file.filename

            except OSError as error:
                # mkdir(path.join(path.dirname(__file__) , 'static' , 'files'))
                file.save(secureFilename(file.filename))
                user.profile_picture = file.filename

            except AttributeError as error:
                user.profile_picture = user.profile_picture
            
            user.about = form.about.data
            user.username = form.username.data
            db.session.commit()
            flash("Profile Have Been Updated" , "success")
            return redirect(url_for('main.profile' , id=current_user.id))
      
        return render_template('ProfileEdit.html' , form=form , user=user)
    else:
        return redirect(url_for('main.login'))
    
@routes.errorhandler(401)
def error(error):
    return render_template('Error.html')


@routes.route("/admin" , methods=['POST' , 'GET'])
@login_required
def admin():

    category_form = CategoryForm()

    category_page = request.args.get('category_page' , 1 , type=int)
    user_page = request.args.get('user_page' , 1 , type=int)
    post_page = request.args.get('post_page' , 1 , type=int)
    reply_page = request.args.get('reply_page' , 1 , type=int)

    users = User.query.paginate(page=user_page , per_page=5)
    posts  = Post.query.paginate(page=post_page , per_page=5)
    replies = Comment.query.paginate(page=reply_page , per_page=5)
    categories = Category.query.paginate(page=category_page , per_page=5)


    if category_form.validate_on_submit():
        category = Category()
        category.title = category_form.title.data
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('main.admin'))

    return render_template(
        'Admin.html' , 
        users=users , 
        posts=posts , 
        categories=categories , 
        replies=replies,
        category_form=category_form
    )


@routes.route('/category/delete/id=<int:id>' , methods=['POST' , 'GET'])
def category_delete(id):
    category = Category.query.filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('main.admin'))


@routes.route('/user/delete/id=<int:id>' , methods=['POST' , 'GET'])
def user_delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.admin'))

@routes.route('/comment/delete/id=<int:id>' , methods=['POST' , 'GET'])
def sudo_reply_delete(id):
    reply = Comment.query.filter_by(id=id).first()
    db.session.delete(reply)
    db.session.commit()
    return redirect(url_for('main.admin'))