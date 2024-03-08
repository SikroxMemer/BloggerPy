from flask import Blueprint, render_template, redirect, url_for , flash
from app.extenstions import login_manager, bcrypt, db
from app.models import (User, Post, Category)
from app.forms import (LoginForm, ReiterationForm, PostForm , EditForm)
from app import (login_required, logout_user, login_user , current_user)


routes = Blueprint('main', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@routes.route('/')
@login_required
def index():
    posts = Post.query.all()
    return render_template('Home.html', posts=posts)


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
def view(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('Post.html', post=post)


@routes.route('/post/delete/id=<int:id>' , methods=['GET' , 'POST'])
def delete(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'message')
    return redirect(url_for('main.index'))

@routes.route('/post/edit/id=<int:id>' , methods=['GET' , 'POST'])
def edit(id):
    categories = Category.query.all()
    choices: list[tuple] = []

    for choice in categories:
        choices.append((choice.id, choice.title))

    post = Post.query.filter_by(id=id).first()
    form = EditForm()

    form.edit_title.data = post.title
    form.edit_story.data = post.story
    form.edit_category.choices = choices
    form.edit_category.default = post.category_id

    if form.validate_on_submit():
        post.title = form.edit_title.data
        post.story = form.edit_story.data
        post.category_id = form.edit_category.data

        db.session.commit()
        flash('Your post has been edited', 'message')
        return redirect(url_for('main.view', id=id))
        ...

    return render_template('Edit.html', post=post , form=form)