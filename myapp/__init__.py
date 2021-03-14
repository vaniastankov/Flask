from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret key different from what I really used'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Sorry. Only Logged Users are Welcome Here:('
login_manager.login_message_category = "danger"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
app.jinja_env.globals.update(zip=zip)
from myapp import routes
