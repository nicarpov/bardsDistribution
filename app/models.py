from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


songs_to_learn = db.Table('songs_to_learn',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)



@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)

    songs_learning = db.relationship(
        'Song', secondary=songs_to_learn,
        backref=db.backref('users_learning', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_song(self, song):
        if not self.is_learning(song):
            self.songs_learning.append(song)

    def remove_song(self, song):
        if self.is_learning(song):
            self.songs_learning.remove(song)

    def is_learning(self, song):
        return self.songs_learning.filter(songs_to_learn.c.song_id == song.id).count() > 0

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return "<Song {}>".format(self.name)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True, nullable=False)
    songs = db.relationship('Song', backref='author', lazy='dynamic')

    def __repr__(self):
        return "<Author {}>".format(self.name)





