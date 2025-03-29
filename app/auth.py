from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import User # From models.py, import User
from app import mongo # From __init__.py, import mongo
from werkzeug.security import generate_password_hash # Flask's hash and verification library

auth = Blueprint('auth', __name__) # Creates a Blueprint (component/module) called 'auth'
