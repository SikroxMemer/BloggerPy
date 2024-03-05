from wtforms import SelectField, StringField, SubmitField, PasswordField, FileField
from wtforms.validators import InputRequired, Length , ValidationError , Optional
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from .models import Category , Post , User

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
