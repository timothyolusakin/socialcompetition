import os
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager,current_user
from flask import Flask,redirect,url_for,render_template,request,current_app
from flask_mail import Mail
from datetime import datetime
import jwt

#initialize packages used in the application
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
#login_manager.login_view = 'index'

#create an initialation of the application
def create_app(config_name):
    # Define the WSGI application object
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Define the database and login manager object which is imported
    # by modules and controllers
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    #Define index for homepage or landing page for visitors
    @app.route('/')
    def index():
        return render_template('index.html')

    #registering admin blueprint for ease of usage
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # registering creatives blueprint for ease of usage
    from .creatives import creatives as creatives_blueprint
    app.register_blueprint(creatives_blueprint, url_prefix='/creatives')

    return (app)