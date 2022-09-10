from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, logout_user
from . import db
import os
auth = Blueprint('auth', __name__)


from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
app = Flask(__name__)


# UPLOAD_FOLDER = 'data/'
# UPLOAD_FOLDER = 'data/rst_files_repo/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@auth.route('/upload')
def upload_file():
   return render_template('pages/upload.html')

@auth.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():

    if request.method == 'POST':
        files = request.files.getlist("file")
        UPLOAD_FOLDER = request.form['path']
# ********* Create Folder on server if not exists
#         print('path')
        # os.makedirs(request.form['path'],exist_ok=False)
        for f in files:
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        return 'Files Uploaded On SERVER Successfully'


@auth.route('/uploaderpm', methods = ['GET', 'POST'])
def upload_file_pm():

    if request.method == 'POST':
        files = request.files.getlist("file")
        UPLOAD_FOLDER = request.form['path']
# ********* Create Folder on server if not exists
#         print('path')
        # os.makedirs(request.form['path'],exist_ok=False)
        for f in files:
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        # return 'Files Uploaded On SERVER SuccessfullyXX'
        flash('Upload successful')
        return redirect('/pmentryflow')




   # if request.method == 'POST':
   #    f = request.files['file']
   #    UPLOAD_FOLDER= request.form['path']
   #    f.save(os.path.join(UPLOAD_FOLDER, f.filename))






if __name__ == '__main__':
   app.run(debug = True)




@auth.route('/login')
def login():
    alldone = True
    return render_template('login.html', alldone=alldone)


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    # return redirect(url_for('main.reliability'))
    # return redirect(url_for('main.availability'))
    return redirect(url_for('main.proj'))


@auth.route('/signup')
def signup():
    return render_template("register.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email').lower()
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    name = first_name + ' ' + last_name
    password = request.form.get('password')
    password2 = request.form.get('password-confirm')
    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if (first_name == ""):
        flash('Please Enter First Name')
        return redirect(url_for('auth.signup'))

    if (last_name == ""):
        flash('Please Enetr Last Name')
        return redirect(url_for('auth.signup'))

    if "alstomgroup" not in email:
        flash('Please Enter Alstom Email ID')
        return redirect(url_for('auth.signup'))

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    if (password == ""):
        flash('Password field cannot be Empty')

    if password != password2:
        flash('Password field not match')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    password_hash = generate_password_hash(password, method='sha256')
    new_user = User(email=email, password=password_hash, name=name)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # flash('User Successfully Registered')

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")


