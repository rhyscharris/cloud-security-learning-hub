from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User # From models.py, import User
from app import mongo # From __init__.py, import mongo
# from werkzeug.security import generate_password_hash # Flask's hash and verification library

auth = Blueprint('auth', __name__) # Creates a Blueprint (component/module) called 'auth'

# WARNING: Demo A - this is intentionally for testing
#password = "secret123" # this is only here to demo Ruff blocking this.

# WARNING: Demo B - this is intentionally for testing
#eval("print('This is insecure')")

@auth.route('/login', methods=['GET', 'POST']) # When user goes to domain or localhost/login, and does POST/GET, do this
def login():
    if current_user.is_authenticated: # Using Flask Login, check user is authenticated (unsurprisingly)
        return redirect(url_for('main.dashboard')) # And then send them to the dashbord (not homepage)
    
    if request.method == 'POST':
        username = request.form.get('username') # Retrieves value of of the 'username' form field
        password = request.form.get('password')
        
        user_data = mongo.db.users.find_one({'username': username}) # Queries MongoDB, map form entry to db record - find_one maps first matching record in the DB
        if user_data and User(user_data).check_password(password): # Check user_data is valid in MongoDB, if so login using user_data, checking password matches stored/hashed one in DB (from models.py). If both OK, continue...
            login_user(User(user_data)) # Log in the user
            next_page = request.args.get('next') # After login, user redirects to main dashboard
            return redirect(next_page or url_for('main.dashboard'))
        flash('Invalid username or password', 'danger') # If incorrect data, flag it
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard')) # If a logged-in user hits register button, just redirect to dashboard
    
    if request.method == 'POST': # Retrieves values entered in form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if mongo.db.users.find_one({'username': username}): # Queries MongoDB, checking if username already exists
            flash('Username already exists', 'danger') # If it does, flash error
            return render_template('register.html') # Exit early as there's an error
        
        if mongo.db.users.find_one({'email': email}): # Same as above, but email
            flash('Email already registered', 'danger')
            return render_template('register.html') # Exit early as there's an error
        
        user_id = User.create_user(username, email, password) # Create the user based on inputted data
        user_data = mongo.db.users.find_one({'_id': user_id}) # Get new user's info via MongoDB
        login_user(User(user_data)) # Creates a User object based on data from MongoDB on above line. Logs in the user, setting up a session to keep user logged-in
        
        flash('Registration successful', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('register.html')

@auth.route('/logout')
@login_required # Obvs a user should be logged-in to view this page (to log-out)
def logout():
    logout_user()
    return redirect(url_for('main.index'))
