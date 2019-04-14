from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


#creatiing blueprint instance:
codes = Blueprint('codes', __name__)

@codes.route('/snake', methods=['GET', 'POST'])
def snake_game():
    return render_template('snake.html', title='Snake')


@codes.route('/contact_me', methods=['GET', 'POST'])
def contact_me():
    return render_template('contact_me.html', title='Contact Alex')

    
