from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

#creatiing blueprint instance:
users = Blueprint('users', __name__)



@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    ##validating user data
    if form.validate_on_submit():#must hash password if user submission is approved:
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #decode in utf8 to turn into string
        user = User(username=form.username.data, email=form.email.data,password=hased_password)#creating for a db
        db.session.add(user)
        db.session.commit()##adding user to database:
        flash('Account has been created! Procede to log in', 'success')
        #redirect user to home page
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        #logging in a user with an email
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #if user exists and password is valid with database:
            login_user(user,remember=form.remember.data)#logs in user and gives remember option form
            next_page = request.args.get('next')#grabs page user was previously on
            return redirect(next_page) if next_page else redirect(url_for('main.home')) #returns user to original page if not put them to the home page
        else:#if login was not sucsessful: send flash message
            flash('Login unsucsessful. Check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        #<begin photo save logic>
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        #</end photo save logic>
        current_user.username = form.username.data
        current_user.email = form.email.data #set new email
        db.session.commit() #submitting changes to the data base
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account') )#redirect so another post isnt sent
    elif request.method =='GET':#populating user form 
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


##user post page route
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=5)##posts per page:
    return render_template('user_posts.html',posts=posts, user=user)


@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #query fist user with eamail:
        send_reset_email(user)
        flash("An email has been sent with password reset instructions", "info")
        return redirect(url_for('users.login')) #returns user to the login page

    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET','POST']) #passing a token through url
def reset_token(token):
    if current_user.is_authenticated: ##making sure the user is logged out
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token) #calls reset token from forms.py 
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():#must hash password if user submission is approved:
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #decode in utf8 to turn into string
        user.password = hased_password #reasinging the password
        db.session.commit()##adding user to database:
        flash('Your password has been updated! Procede to log in', 'success')
        #redirect user to home page
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)