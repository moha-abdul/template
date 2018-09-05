from flask import render_template
from . import auth

@auth.route('/auth')
def login():
    
    return render_template('auth/login.html')