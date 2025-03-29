from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Quiz

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    quizzes = Quiz.get_all_quizzes()
    user_results = Quiz.get_user_results(current_user.get_id())
    completed_quizzes = [r['quiz_id'] for r in user_results]
    
    return render_template(
        'dashboard.html',
        user=current_user,
        quizzes=quizzes,
        completed_quizzes=completed_quizzes
    )
