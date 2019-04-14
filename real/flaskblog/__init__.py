#alex Shelton
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail 
from flaskblog.config import Config



#sql alchemy instance
db = SQLAlchemy()
bcrypt = Bcrypt()#initialiaing hashing
login_manager = LoginManager()#login manager so users can log in
login_manager.login_view = 'users.login' ##passing in function name of route if user isnt logged in
login_manager.login_message_category = 'warning' #warning = yellow color


mail = Mail() #initialize






#function to create a flask app:
def create_app(config_class=Config):
    app = Flask(__name__) # __name__ = name of module
    app.config.from_object(Config) ##configures the Flask app from the config class in the file, can create multiple instances of the flask app

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    #importing blueprint instances
    from flaskblog.users.routes import users 
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors #instance of errors blueprint. similar for the rest of the imports
    from flaskblog.codes.routes import codes
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(codes)

    return app

    

