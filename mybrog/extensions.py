from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_moment import Moment
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()
debug = DebugToolbarExtension()


@login_manager.user_loader
def load_user(user_id):
    from mybrog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
