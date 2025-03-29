import os

class Config:
     # Set these in dockerfile or env as otherwise it uses unsecure defaults
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development-key-change-in-production'
    # OLD MONGO_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/security_hub'
    MONGO_URI = os.environ.get('MONGODB_URI') or 'mongodb://admin:password@mongodb:27017/security_hub?authSource=admin' # new