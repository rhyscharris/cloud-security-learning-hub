from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config

mongo = PyMongo() # Creates PyMongo instance (not initialised yet)

def create_app(config_class=Config):
    app = Flask(__name__) # creates instance of Flask
    app.config.from_object(config_class) # load config from settings defined in 'config_class' 
    
    mongo.init_app(app) # Initialise PyMongo
    
    # Import blueprints (components/modules) for different sections of the application
    from app.routes import main
    
    # Register blueprints (components/modules) for different sections of the application
    app.register_blueprint(main)
    
    return app