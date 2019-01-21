

from flask import Flask 
from datetime import datetime
from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from . import app, lm 
from .models import User, enduser, Arglist, Role
from .forms import LoginForm, SignupForm, AddNoteForm, surveyForm, argumentsForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)



"""
Routes and views for the flask application.
"""
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new = User(username=form.username.data, email=form.email.data, password=form.password.data)
        new.save()
        flash("Registration was successful")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Login successful")
            return redirect(url_for('home'))
        flash("Incorrect password or email")
    return render_template('login.html', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/home')
def home():
    """Renders the home page."""
  
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/survey', methods=['POST','GET'])
def survey():
    form = surveyForm()
    if form.validate_on_submit():
        new = enduser(name=form.name.data, nationality=form.nationality.data, gender=form.gender.data, age=form.age.data)
        new.save()
        flash("Survey was successful")
        return redirect(url_for('experiments'))
    return render_template(
        'survey.html', 
        form=form,
        year=datetime.now().year
        )

@app.route('/Experiments')
def experiments():
    """Renders the home page."""

    return render_template(
        'roomExp.html',
        title='Experiment page',

        year=datetime.now().year,
    )


@login_required
@app.route('/arguments')
def arguments():
    """Save new arguments."""
    form = argumentsForm()
   
    if form.validate_on_submit():
        new_arg = Arglist(side=form.side.data, title=form.title.data, claim=form.claim.data)
        new_arg.save()
        return redirect(url_for('experiments'))
        
    return render_template(
        'arguments.html',
        form=form,
        title='arguments to render',
        year=datetime.now().year,
    )


@app.route('/dialogs')
def dialogs():
  """Renders the home page."""
  return render_template(
    'show.html',
    year=datetime.now().year,
    )
    
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
