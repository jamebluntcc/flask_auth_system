from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_webpack import Webpack


login_manager = LoginManager()
migrate = Migrate()
db = SQLAlchemy()
bcrypt = Bcrypt()
webpack = Webpack()