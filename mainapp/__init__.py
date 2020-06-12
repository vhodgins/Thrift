from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager





app = Flask(__name__)
app.config['SECRET_KEY'] = '3a1940fd367d18750997701db5993f87'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thriftsite.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from mainapp import routes
