import models
import hashlib
from app import db


def check_signup_form_errors(request):
    username = request.form['username']
    password1 = request.form['password']
    password2 = request.form['confirm_password']
    if password1 != password2:
        return 'Passwords do not match.'
    else:
        user = models.User.query.filter_by(username=username).first()
        if user:
            return 'Username already taken.'
    return ''


def create_user(request):
    username = request.form['username']
    password = request.form['password']
    user = models.User(username=username, password=hashlib.md5(password.encode()).hexdigest())
    db.session.add(user)
    db.session.commit()


def authenticate(username, password):
    user = models.User.query.filter_by(username=username, password=hashlib.md5(password.encode()).hexdigest()).first()
    if user:
        return user
