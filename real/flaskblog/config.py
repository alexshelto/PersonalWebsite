#alex shelton

#create enviornment variables for production

class Config:
    SECRET_KEY = '' ##secret key login stuff
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' #3 slashes = relative path
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 #465 = ssl number 587=TLS
    MAIL_USE_TLS = True ##using a transport layer security
    #MAIL_USE_SSL = True
    #Delete if you release code~~~~~~~~~~~~~~~~~~~~~~~~~~
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
