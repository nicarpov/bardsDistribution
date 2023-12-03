from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import current_user, login_user
import sqlalchemy as sa


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Sign In')


@app.route('/signup')
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Registration requested by user {}, remember_me {}'
              .format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            redirect(url_for('signin'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('signin.html', title='Sign In', form=form)
