from flask import render_template , redirect , url_for , flash , request
from flask_login import login_user , logout_user , login_required
from . import auth

from .. import db
from ..models import User
from .forms import RegistrationForm , LoginForm



@auth.route('/auth' ,methods=["GET","POST"])
def login():
    login_form = LoginForm()
    title = 'Watchlist Login'
    
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()

        if user is not None and user.verify_password( login_form.password.data ):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        
        flash ("Invalid username or password")
    
    return render_template('auth/login.html' , login_form = login_form, title = title)


''''
    Route for loggin out users and redirect them to the index.html / home page
'''
@auth.route('/logged-out')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=["GET","POST"])
def register():

    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))

        title = "New Account"

    return render_template('/auth/register.html' ,title=title, register_form = form)