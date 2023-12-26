from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, AddSong
from app.models import User, Song, Author
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit



@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Sign In')


@app.route('/explore')
def explore():
    songs = Song.query.join(Author).order_by(Author.name.asc()).all()
    return render_template('explore.html', songs=songs)


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect('/signin')
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if current_user.is_authenticated:

        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('signin'))

        login_user(user, remember=form.remember_me.data)
        flash("Login successful")
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('signin.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    user = current_user
    return render_template('profile.html', user=user, title='User Profile')


@app.route('/add_song', methods=["GET","POST"])
def add_song():
    form = AddSong()

    if form.validate_on_submit():
        author_query = Author.query.filter_by(name=form.author.data)
        author = None
        if author_query.count() > 0:
            author = author_query.first()
        else:
            author = Author(name=form.author.data)
            db.session.add(author)
        song = Song(name=form.name.data, author=author)
        db.session.add(song)

        current_user.add_song(song)
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('add_song.html', form=form)


@app.route('/mark')
def mark():



