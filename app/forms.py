from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
import sqlalchemy as sa
from app import db
from app.models import User, Song, Author


class LoginForm(FlaskForm):
    username = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Next")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is None:
            raise ValidationError("Please enter different username")


class RegisterForm(FlaskForm):
    username = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Next")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Please enter different username")


class AddSong(FlaskForm):
    name = StringField("Song name:", validators=[DataRequired()])
    author = StringField("Author name:", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_name(self, name):
        name = db.session.scalar(sa.select(Song).where(Song.name == name.data))
        author = db.session.scalar(sa.select(Author).where(Author.name == self.author.data))

        if name is not None and author is not None:
            raise ValidationError("Song already exists. Add another song")

