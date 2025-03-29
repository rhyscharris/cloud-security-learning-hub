# Cloud Security Learning Hub

A containerized Flask application that provides an interactive testing/learning platform for cloud security concepts. This 3-tier application uses Python, Flask, MongoDB, HMTL/JS (including Bootstrap) and is designed for deployment on AWS EKS eventually.

## Features

- User authentication (register, login, logout)
- Interactive cloud security quizzes
- Score tracking, quiz results, and progress monitoring
- Responsive UI with Bootstrap and some custom HTML/CSS
- Containerized for easy deployment

## Tech Stack

- **Backend**: Python, Flask
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Containerization**: Docker, Kubernetes

## Project Structure

- `app/`: Main application code
  - `__init__.py`: Flask application initialization
  - `config.py`: Configuration settings
  - `models.py`: Data models for MongoDB
  - `routes.py`: Main application routes
  - `auth.py`: Authentication functionality
  - `quiz.py`: Quiz functionality
  - `static/`: Static assets (CSS, JS, images)
  - `templates/`: HTML templates (e.g. main)
- `kubernetes/`: Kubernetes configuration for EKS
- `Dockerfile`: Container definition
- `docker-compose.yml`: Local development setup
- `requirements.txt`: Project dependencies
- `scripts/`: Automation scripts for database, backups, etc

## License

MIT
