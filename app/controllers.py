from abc import ABC

from app.forms import (
    PostForm , 
    LoginForm , 
    ReiterationForm , 
    CategoryForm , 
    ReplyForm , 
    EditForm , 
    ProfileForm
)



from app.models import Category , Post , User , Comment
from app import db
from flask import flash , render_template , redirect , url_for , request


from flask_login import current_user , login_user , logout_user
from app import bcrypt
from app.settings import UPLOAD_FOLDER

from werkzeug.utils import secure_filename

from os import path

def secureFilename(filename:str):
    __DIR__ = path.join(path.abspath(path.dirname(__file__)) , UPLOAD_FOLDER , secure_filename(filename=filename))
    return __DIR__


class AbstractController(ABC):
    @staticmethod
    def store():
        ...
    @staticmethod
    def create():
        ...
    @staticmethod
    def view():
        ...
    @staticmethod
    def edit():
        ...
    @staticmethod
    def destroy():
        ...

class PostController(AbstractController):
    @staticmethod
    def create():
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
            flash("You've successfully created a post ", "success")
            return redirect(url_for('main.index'))
        return render_template('post.create.html', form=form)
    

    @staticmethod
    def view(id):
        page = request.args.get('page' , 1 , type=int)
        post = Post.query.filter_by(id=id).first()
        replies = Comment.query.filter_by(post=post).paginate(page=page , per_page=5)
        return render_template('post.html', post=post , replies=replies)
    
    @staticmethod
    def edit(id : int):
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
        
        return render_template('post.edit.html', post=post , form=form)

    @staticmethod
    def destroy(id):
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        flash("You've successfully deleted your post", 'warning')
        return redirect(url_for('main.index'))
    
    @staticmethod
    def close(id):
        post = Post.query.get(id)
        post.active = False
        db.session.commit()
        return redirect(url_for('main.view' , id=id))
    


class AuthController:
    @staticmethod
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    flash("You've Successfully Loged In !" , "success")
                    if user.type == 'User':
                        return redirect(url_for('main.index'))
                    else:
                        return redirect(url_for('main.admin'))
                else:
                    flash("Wrong Credentials , please check your email or password" , "danger")
            else:
                flash("No such user exists with the current credentials" , "warning")
        return render_template('login.html', form=form)
    
    @staticmethod
    def register():
        form = ReiterationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data,password=hashed_password, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            flash("You've successfully created an account", "success")
            return redirect(url_for('main.login'))
        return render_template('register.html', form=form)
    
    @staticmethod
    def logout():
        logout_user()
        flash("You've Successfully Loged Out" , "success")
        return redirect(url_for('main.login'))
    



class ReplyController():
    @staticmethod
    def create(id):
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
        return render_template('post.reply.html', post=post , form=form)
  
        
    @staticmethod
    def destroy(id , post):
        reply = Comment.query.filter_by(id=id).first()
        db.session.delete(reply)
        db.session.commit()
        flash('Reply Deleted' , 'info')
        return redirect(url_for('main.view' , id=post))


class ProfileController():
    @staticmethod
    def edit():
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
            return redirect(url_for('main.view_profile' , id=current_user.id))
        return render_template('profile.edit.html' , form=form , user=user)
    @staticmethod
    def view(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            flash('No User with the ID : {} Found !'.format(id) , 'danger')
            return redirect(url_for('main.index'))
        return render_template('profile.html' , user=user)