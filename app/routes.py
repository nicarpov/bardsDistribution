from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, AddSong, EmptyForm, EditProfile
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
    songs = Song.query.join(Author).order_by(Author.name)\
        .order_by(Song.name)
    form = EmptyForm()
    return render_template('explore.html', songs=songs, form=form)


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)

        db.commit()
        flash('Registration requested by user {}, remember_me {}'
              .format(form.username.data))

        db.session.commit()
        return redirect('/signin')
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if current_user.is_authenticated:

        return redirect(url_for('explore'))

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
            next_page = url_for('explore')
        return redirect(next_page)
    return render_template('signin.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
def user(username):
    user = User.query.filter(User.username == username).first()
    songs = user.songs_learning.join(Author, Song.author_id == Author.id).order_by(Author.name)\
        .order_by(Song.name)
    form = EmptyForm()
    return render_template('user.html', user=user, songs=songs,
                           title='User Profile', form=form)


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


@app.post('/mark/<song_id>')
def mark(song_id):
    form = EmptyForm()
    if form.validate_on_submit():
        song = Song.query.filter_by(id=song_id).first()
        if song is None:
            flash('There is no song with id {}'.format(song_id))
            return redirect(url_for('index'))

        current_user.add_song(song)
        db.session.commit()

        return redirect(url_for('explore'))


@app.post('/unmark/<song_id>')
def unmark(song_id):
    form = EmptyForm()
    if form.validate_on_submit():
        song = Song.query.filter_by(id=song_id).first()
        if song is None:
            flash('There is no song with id {}'.format(song_id))
            return redirect(url_for('index'))

        current_user.remove_song(song)
        db.session.commit()
        return redirect(url_for('explore'))


@app.route('/edit_profile', methods=['GET','POST'])
def edit_profile():
    form = EditProfile()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash("Your changes applied successfully!")
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name or ""
        form.last_name.data = current_user.last_name or ""
    return render_template('edit_profile.html', form=form)




