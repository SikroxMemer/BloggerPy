from flask import Blueprint, render_template, redirect, url_for , flash , request
from app.extenstions import login_manager, bcrypt, db
from app.models import (User, Post, Category , Comment)
from app.forms import (LoginForm, ReiterationForm, PostForm , EditForm , ReplyForm)
from app import (login_required, logout_user, login_user , current_user)


routes = Blueprint('main', __name__, template_folder='templates')


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
        posts = Post.query.paginate(page=page , per_page=3)
        return render_template('Home.html', posts=posts)
    else:
        return redirect(url_for('main.login'))

    


@routes.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.index'))

    return render_template('Login.html', form=form)


@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = ReiterationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Your account has been created!", "message")

        return redirect(url_for('main.login'))

    return render_template('Register.html', form=form)


@routes.route('/post/create', methods=['GET', 'POST'])
@login_required
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

        flash("Your post has been created!", "message")

        return redirect(url_for('main.index'))
    return render_template('Create.html', form=form)


@routes.route('/post/view/id=<int:id>' , methods=['POST' , 'GET'])
@login_required
def view(id):
    post = Post.query.filter_by(id=id).first()
    replies = Comment.query.filter_by(post=post)
    return render_template('Post.html', post=post , replies=replies)


@routes.route('/post/delete/id=<int:id>' , methods=['GET' , 'POST'])
@login_required
def post_delete(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'message')
    return redirect(url_for('main.index'))

@routes.route('/post/edit/id=<int:id>' , methods=['GET' , 'POST'])
def post_edit(id):
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
        flash('Your post has been edited', 'message')
        return redirect(url_for('main.view', id=id))
        ...

    return render_template('Edit.html', post=post , form=form)


@routes.route('/post/reply/id=<int:id>' , methods=['GET' , 'POST'])
def reply(id):
    form = ReplyForm()
    post = Post.query.filter_by(id=id).first()

    if form.validate_on_submit():
        story = form.story.data
        reply = Comment()

        reply.comment_owner = post.post_owner
        reply.comment = story
        reply.post = post

        db.session.add(reply)
        db.session.commit()

        return redirect(url_for('main.view' , id=id))

    return render_template('Reply.html', post=post , form=form)


@routes.route('/reply/delete/id=<int:id>' , methods=['GET' , 'POST'])
def reply_delete(id):
    reply = Comment.query.filter_by(id=id).first()
    db.session.delete(reply)
    db.session.commit()
    flash('Reply Deleted' , 'message')
    return redirect(url_for('main.index'))


@routes.route('/profile/view/id=<int:id>'  , methods=['GET' , 'POST'])
def profile(id):
    user = User.query.filter_by(id=id).first()
    return render_template('Profile.html' , user=user)