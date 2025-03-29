from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from app.config import Config

mongo = PyMongo() # Creates PyMongo instance (not initialised yet)
login_manager = LoginManager() # Creates Flask LoginManager instance (not initialised yet)
login_manager.login_view = 'auth.login' # Un-logged-in users hit login page
login_manager.login_message_category = 'info' # login warning message set to 'info' category

def create_app(config_class=Config):
    app = Flask(__name__) # creates instance of Flask
    app.config.from_object(config_class) # load config from settings defined in 'config_class' 
    
    mongo.init_app(app) # Initialise PyMongo
    login_manager.init_app(app) # Initialise LoginManager
    
    # Import blueprints (components/modules) for different sections of the application
    from app.routes import main
    from app.auth import auth
    from app.quiz import quiz
    
    # Register blueprints (components/modules) for different sections of the application
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(quiz)
    
    return app