from wtforms import SelectField, StringField, SubmitField, PasswordField, FileField
from wtforms.validators import InputRequired, Length, ValidationError, Optional
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from .models import Category, Post, User


class ReiterationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=70)], render_kw={"placeholder": "Username", "class": "form-control"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=7, max=20)], render_kw={"placeholder": "Password", "class": "form-control"})
    email = StringField(validators=[InputRequired(), Length(
        min=6, max=70)], render_kw={"placeholder": "Email", "class": "form-control"})

    submit = SubmitField("Register", render_kw={
                         "class": "btn btn-primary form-control"})

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
        "placeholder": "Email", "class": "form-control"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=7, max=20)], render_kw={"placeholder": "Password", "class": "form-control"})

    submit = SubmitField("Login", render_kw={
                         "class": "btn btn-primary form-control"})


class PostForm(FlaskForm):

    

    title = StringField(validators=[InputRequired(), Length(
        min=4, max=70)], render_kw={"placeholder": "Title", "class": "form-control"})

    story = CKEditorField(validators=[InputRequired(), Length(
        min=4, max=5000)], render_kw={"placeholder": "Story"})

    category = SelectField(validators=[InputRequired()], render_kw={
                           "class": "form-control"})

    submit = SubmitField("Post", render_kw={
                         "class": "btn btn-primary form-control"})


class ReplyForm(FlaskForm):
    ...


class EditForm(FlaskForm):
    edit_title = StringField(render_kw={"placeholder": "Title", 'class': 'form-control'})
    edit_story = CKEditorField()
    edit_category = SelectField(render_kw={'class': 'form-control'})
    edit_submit = SubmitField("Modify", render_kw={'class': 'btn btn-primary form-control'})


class ProfileForm(FlaskForm):
    username = StringField(
        render_kw={"placeholder": "Username", 'disabled': True, 'class': "form-control"})
    email = StringField(render_kw={"placeholder": "Email", 'disabled': True})
    profile_picture = FileField('File', validators=[Optional()])
    about = CKEditorField()
    submit = SubmitField("Modifier")
