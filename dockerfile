FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy required files for security (also configure .dockerignore for extra security)

# COPY . . # ONLY USE THIS FOR DEV SETUP FOR INITIAL DATABASE DATA
COPY app/ ./app/
COPY wsgi.py .

EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]