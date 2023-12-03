from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm, RegisterForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Sign In')


@app.route('/signup')
def signup():
    form = RegisterForm()
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested by user {}, remember_me {}'
              .format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('signin.html', title='Sign In', form=form)