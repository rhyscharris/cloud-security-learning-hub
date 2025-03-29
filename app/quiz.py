from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Quiz # From models.py import Quiz
from app import mongo # From __init__.py import mongo
from bson.objectid import ObjectId # MongoDB ObjectId - in this case used for finding User IDs (see below)

quiz = Blueprint('quiz', __name__)

@quiz.route('/quiz/<quiz_id>')
@login_required
def take_quiz(quiz_id):
    quiz_data = Quiz.get_quiz(quiz_id) # Gets data from DB about this quiz_id
    if not quiz_data: # If no data found, show error, redirect to dashboard. Doesn't see to work though (server error)
        flash('Quiz not found', 'danger')
        return redirect(url_for('main.dashboard'))
    
    results = list(mongo.db.quiz_results.find({
        'user_id': ObjectId(current_user.get_id()), # Store user ID to MongoDB's ObjectID
        'quiz_id': ObjectId(quiz_id) # Store quiz ID to MongoDB's OBjectID
    }))
    
    # Check if user already completed this quiz
    if results: # If results for this user exist
        flash('You have already completed this quiz', 'info') # Tell them
        return redirect(url_for('quiz.results', result_id=results[0]['_id'])) # And redirect them to show their results
    
    return render_template('quiz.html', quiz=quiz_data) # But if they haven't completed it, show quiz

@quiz.route('/quiz/<quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz_data = Quiz.get_quiz(quiz_id) # Get quiz data from DB
    if not quiz_data:
        flash('Quiz not found', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user_answers = {}
    score = 0
    
    for question in quiz_data['questions']:
        q_id = str(question['_id']) # Convert question ID to string
        user_answer = request.form.get(q_id) # Gather user's answer from form
        user_answers[q_id] = user_answer # And then store in a dictionary
        
        if user_answer == question['correct_answer']: # If user's answer matches correct answer in DB...
            score += 1 # increment score
    
    # Calculate percentage score
    max_score = len(quiz_data['questions'])
    percentage_score = int((score / max_score) * 100)
    
    # Save results to DB
    result_id = Quiz.save_quiz_result(
        current_user.get_id(), 
        quiz_id, 
        percentage_score,
        user_answers
    )
    
    # Update user's total score
    current_user.update_score(percentage_score)
    
    flash(f'Quiz completed! Your score: {percentage_score}%', 'success')
    return redirect(url_for('main.dashboard'))

@quiz.route('/results/<result_id>')
@login_required
def results(result_id):
    result = mongo.db.quiz_results.find_one({'_id': ObjectId(result_id)}) # find this user's result
    if not result or result['user_id'] != ObjectId(current_user.get_id()): # If result doesn't exist, or doesn't to this user...
        flash('Result not found', 'danger')
        return redirect(url_for('main.dashboard'))
    
    quiz_data = Quiz.get_quiz(str(result['quiz_id']))
    
    return render_template('results.html', result=result, quiz=quiz_data)
