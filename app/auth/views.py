from flask import render_template , redirect , url_for
from . import auth

from .. import db
from ..models import User
from .forms import RegistrationForm



@auth.route('/auth')
def login():
    
    return render_template('auth/login.html')


@auth.route('/register', methods=["GET","POST"])
def register():

    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))

        title = "New Account"

    return render_template('/auth/register.html' , register_form = form)