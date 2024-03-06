"""

# Blogger 1.0.0v
By Sikrox Memer 2024

"""
from flask_login import (login_user, logout_user,
                         LoginManager, current_user, login_required)
from flask import (Flask, render_template, url_for, redirect)

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    FileField,
    SelectField,
    Label,
    BooleanField
)

from wtforms.validators import (
    InputRequired, Length, ValidationError, Optional)
from flask_wtf import (FlaskForm)
from flask_ckeditor import (CKEditorField)


from flask_ckeditor import (CKEditor)
from flask_bcrypt import (Bcrypt)
from werkzeug.utils import secure_filename
from os import path
from rich.console import Console


conosle = Console()

# __MAIN__ (TOP_LEVEL)

app = Flask(__name__)
ckeditor = CKEditor(app)
login_manager = LoginManager()

bcrypt = Bcrypt(app)

app.app_context().push()
__DIR__ = path.abspath(path.dirname(__file__))

# CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = 'SEC RET_KEY'
app.config['UPLOAD_FOLDER'] = 'static/files'
login_manager.login_view = "login"

db = SQLAlchemy(app)

login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(70), unique=True, nullable=False)
    about = db.Column(db.String(5000), nullable=True)

    def __repr__(self) -> str:
        return '<User %r>' % self.id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)

    def __repr__(self) -> str:
        return '<Category %r>' % self.id


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55), nullable=False)
    story = db.Column(db.String(5000), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref(
        'post', cascade='all, delete-orphan'))

    post_date = db.Column(db.Date, default=db.func.current_date())

    post_owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    post_owner = db.relationship('User', backref=db.backref(
        'post', cascade='all, delete-orphan'))

    def __repr__(self) -> str:
        return '<Post %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(150), nullable=False)

    comment_date = db.Column(db.Date, default=db.func.current_date())
    comment_owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    comment_owner = db.relationship('User', backref=db.backref(
        'comment', cascade='all, delete-orphan'))

    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    post = db.relationship('Post', backref=db.backref(
        'comment', cascade='all, delete-orphan'))

    def __repr__(self) -> str:
        return '<Comment %r>' % self.id


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    post = db.relationship('Post', backref=db.backref(
        'rating', cascade='all, delete-orphan'))
    positive = db.Column(db.Integer, default=0)
    negative = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'), unique=True, nullable=False)
    user = db.relationship('User', backref=db.backref(
        'rating', cascade='all, delete-orphan'))


db.create_all()


class RegiterationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=70)], render_kw={"placeholder": "Username", "class": "form-control"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=7, max=20)], render_kw={"placeholder": "Password", "class": "form-control"})
    email = StringField(validators=[InputRequired(), Length(
        min=6, max=70)], render_kw={"placeholder": "Email", "class": "form-control"})

    submit = SubmitField("Register", render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        existing_user = User.query.filter_by(
            username=username.data
        ).first()

        if existing_user:
            raise ValidationError(
                "Username already exists , Please Chose Another One"
            )


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=70)], render_kw={
                        "placeholder": "Email"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=7, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login", render_kw={"class": "btn btn-primary"})


class PostForm(FlaskForm):
    category = Category.query.all()
    title = StringField(validators=[InputRequired(), Length(
        min=4, max=70)], render_kw={"placeholder": "Title"})

    story = CKEditorField(validators=[InputRequired(), Length(
        min=4, max=5000)], render_kw={"placeholder": "Story"})

    select: list[tuple] = []
    for item in category:
        select.append((item.id, item.title))

    category = SelectField(validators=[InputRequired()], choices=select)

    submit = SubmitField("Poste")


class ReplyForm(FlaskForm):
    ...


class EditForm(FlaskForm):

    category = Category.query.all()
    select: list[tuple] = []

    edit_title = StringField(
        render_kw={"placeholder": "Title", 'class': 'form-control'})
    edit_story = CKEditorField()

    edit_submit = SubmitField("Modifier", render_kw={
                              'class': 'btn btn-primary'})


class ProfileForm(FlaskForm):
    username = StringField(
        render_kw={"placeholder": "Username", 'disabled': True, 'class': "form-control"})
    email = StringField(render_kw={"placeholder": "Email", 'disabled': True})
    profile_picture = FileField('File', validators=[Optional()])
    about = CKEditorField()
    submit = SubmitField("Modifier")


@app.route('/newPost', methods=['POST', 'GET'])
@login_required
def NewPost():
    """
    Route for creating a new post. Handles both POST and GET requests. 
    Requires login. 
    Validates form input and saves the file to the upload folder. 
    Creates a new Post object and adds it to the database. 
    Returns a redirect or renders the NewPost.html template.
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            story=form.story.data,
            category_id=int(form.category.data),
            post_owner_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('NewPost.html', form=form)


@app.route('/')
@login_required
def home():
    """
    Route for the home page, requires login.
    """
    user = User.query.get_or_404(current_user.id)
    posts = db.session.query(
        Post.id, Post.title,
        Post.story,
        Post.post_owner_id,
        Post.post_date,
        User.username,
        Category.title.label('category'),
    ).join(User, User.id == Post.post_owner_id).join(Category, Category.id == Post.category_id).all()

    return render_template('home.html', posts=posts, user=user)


@login_manager.user_loader
def load_user(user_id):
    """
    Function to load a user based on the user_id.
    Parameters:
    - user_id: The id of the user to be loaded.
    Returns:
    - User: The user object associated with the user_id.
    """
    return User.query.get(int(user_id))


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            
    return render_template('Login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegiterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('Register.html', form=form)


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


@app.route('/post/<int:id>', methods=['POST', 'GET'])
@login_required
def post(id):
    user = User.query.get_or_404(current_user.id)
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post, user=user)


@app.route('/reply/<int:id>', methods=['POST', 'GET'])
@login_required
def reply(id):
    ...


# POTENTIAL_BUG !!

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id):
    form = EditForm()
    post: Post = Post.query.get_or_404(id)
    form.edit_story.data = post.story
    form.edit_title.data = post.title
    if form.validate_on_submit():
        db.session.query(Post).filter_by(id=id).update(
            {'title': form.edit_title.data,
             'story': form.edit_story.data,
             })
        conosle.print('[red]DITED[/]')
        db.session.commit()
        return render_template('modify.html', post=post, form=form)
    return render_template('modify.html', post=post, form=form)


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = ProfileForm()
    user = User.query.get_or_404(current_user.id)
    if form.validate_on_submit():
        file = form.profile_picture.data
        if file.filename == '':
            db.session.query(User).filter_by(
                id=current_user.id).update({'about': form.about.data})
            db.session.commit()
        else:
            file.save(path.join(path.abspath(path.dirname(__file__)),
                                app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

            db.session.query(User).filter_by(id=current_user.id).update(
                {'profile_picture': file.filename, 'about': form.about.data})
            db.session.commit()
        return redirect(url_for('home'))

    return render_template('profile.html', user=user, form=form)


if __name__ == "__main__":

    app.run(debug=True)
