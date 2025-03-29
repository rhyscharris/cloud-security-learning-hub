# This .py focusses on users and DB connectivity

from flask_login import UserMixin # Import this Flask-Login module (it provides session management, such as 'is_active' or 'is_authenticated')
from werkzeug.security import generate_password_hash, check_password_hash # Auth/Hashing module, doing hashing in this case
from app import mongo, login_manager # From __init__.py, import mongo
from bson.objectid import ObjectId # MongoDB ObjectId - in this case used for finding User IDs (see below)
import datetime

@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({"_id": ObjectId(user_id)}) # Find user in MongoDB based in their User ID
    if not u:
        return None # If no user found, return None
    return User(u) # If user found, return user data

class User(UserMixin): # Creates User class, which inherits from UserMixin to provide session mgmt
    def __init__(self, user_data): # Initialises user Object with data in DB
        self.user_data = user_data # Store user data (from DB) in the Object just created
        
    def get_id(self): # Retrieve user's unique ID
        return str(self.user_data.get('_id')) # And return it as a string
    
    @property
    def is_authenticated(self): # Return whether user is authenticate
        return True # Always returns true in this app
        
    @property
    def is_active(self):
        return True # User is always considered active in this app
        
    @property
    def is_anonymous(self):
        return False
    
    @property
    def username(self):
        return self.user_data.get('username') # Get user's username from user_data
    
    @property
    def email(self):
        return self.user_data.get('email')
    
    @property
    def total_score(self):
        return self.user_data.get('total_score', 0) # Return user's score. Default score to 0 if no score found
    
    @property
    def quizzes_completed(self):
        return self.user_data.get('quizzes_completed', 0) # Same as above but quizzes
    
    @staticmethod
    def create_user(username, email, password):
        # Create new user in the DB
        user = {
            'username': username, 
            'email': email,
            'password_hash': generate_password_hash(password), # Hash password for security
            'total_score': 0,
            'quizzes_completed': 0,
            'created_at': datetime.datetime.utcnow()
        }
        # Insert user into MongoDB, return new user ID
        user_id = mongo.db.users.insert_one(user).inserted_id
        return user_id
    
    # Check provided password matches stored hash
    def check_password(self, password): # Utilised in auth.py
        return check_password_hash(self.user_data.get('password_hash'), password)
    
    def update_score(self, score):
        mongo.db.users.update_one(
            {'_id': ObjectId(self.get_id())}, # find user by their ObjectID
            {'$inc': {'total_score': score, 'quizzes_completed': 1}} # Increment score & quizzes completed
        )
    
class Quiz:
    @staticmethod
    def get_quiz(quiz_id):
        # Get specific quiz based on its ID
        return mongo.db.quizzes.find_one({"_id": ObjectId(quiz_id)})
    
    @staticmethod
    def get_all_quizzes():
        return list(mongo.db.quizzes.find())
    
    @staticmethod
    def get_questions(quiz_id):
        # Get all questions for specific quiz based on its ID
        quiz = mongo.db.quizzes.find_one({"_id": ObjectId(quiz_id)})
        if quiz:
            return quiz.get('questions', []) # Return questions as an array
        return [] # Return empty array if quiz not found
    
    @staticmethod
    def save_quiz_result(user_id, quiz_id, score, answers):
        result = {
            'user_id': ObjectId(user_id),
            'quiz_id': ObjectId(quiz_id),
            'score': score,
            'answers': answers,
            'completed_at': datetime.datetime.utcnow()
        }
        # Put result in DB
        mongo.db.quiz_results.insert_one(result)
    
    @staticmethod
    # for specific user
    def get_user_results(user_id):
        return list(mongo.db.quiz_results.find({'user_id': ObjectId(user_id)}))
