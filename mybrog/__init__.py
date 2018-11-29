import os

from flask import Flask
from mybrog.settings import config
from mybrog.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate, debug
from mybrog.commands import register_commands
from mybrog.models import db, Admin, Post, Category, Comment, Link
from flask_login import current_user
from mybrog.blueprints.blog import blog_bp
from mybrog.blueprints.admin import admin_bp
from mybrog.blueprints.auth import auth_bp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('mybrog')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_template_context(app)
    register_blueprints(app)
    register_shell_context(app)
    register_commands(app)

    return app



def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    debug.init_app(app)



def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)



def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        posts = Post.query.order_by(Post.id).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, links=links, unread_comments=unread_comments)



