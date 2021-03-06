from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_mail import Mail

login_manager = LoginManager()
migrate = Migrate()
db = SQLAlchemy()
bcrypt = Bcrypt()
admin = Admin()
mail = Mail()