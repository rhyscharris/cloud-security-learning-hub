"""
Script to initialize the MongoDB database with sample quiz data.
Run this after deploying the application to set up initial content.
"""

from pymongo import MongoClient
import datetime
from bson import ObjectId
import os

# MongoDB connection string from environment or use default for local development
mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://admin:password@localhost:27017/security_hub?authSource=admin')

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client.get_database()

# Sample quizzes for cloud security
quizzes = [
    {
        "_id": ObjectId(),
        "title": "AWS Security Fundamentals",
        "description": "Test your knowledge of AWS security basics and best practices.",
        "difficulty": "Beginner",
        "created_at": datetime.datetime.utcnow(),
        "questions": [
            {
                "_id": ObjectId(),
                "text": "Which AWS service is primarily used for managing user access and permissions?",
                "type": "multiple_choice",
                "options": ["EC2", "S3", "IAM", "VPC"],
                "correct_answer": "IAM",
                "explanation": "AWS Identity and Access Management (IAM) enables you to manage access to AWS services and resources securely."
            },
            {
                "_id": ObjectId(),
                "text": "What is the AWS shared responsibility model?",
                "type": "multiple_choice",
                "options": [
                    "AWS is responsible for all security aspects of the cloud",
                    "Customers are responsible for all security aspects of the cloud",
                    "AWS is responsible for security of the cloud, customers are responsible for security in the cloud",
                    "Security is only needed at the application level"
                ],
                "correct_answer": "AWS is responsible for security of the cloud, customers are responsible for security in the cloud",
                "explanation": "The shared responsibility model distinguishes between AWS's responsibility 'of' the cloud (infrastructure) and the customer's responsibility 'in' the cloud (data, configuration)."
            },
            {
                "_id": ObjectId(),
                "text": "Which of the following is a best practice for securing AWS S3 buckets?",
                "type": "multiple_choice",
                "options": [
                    "Always make buckets public",
                    "Use bucket policies and IAM policies to restrict access",
                    "Store credentials in S3 buckets for easy access",
                    "Disable encryption to improve performance"
                ],
                "correct_answer": "Use bucket policies and IAM policies to restrict access",
                "explanation": "Using bucket policies and IAM policies allows you to control who can access your S3 resources."
            },
            {
                "_id": ObjectId(),
                "text": "By default, S3 buckets are publicly accessible.",
                "type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "By default, S3 buckets are private and require explicit permissions to allow public access."
            },
            {
                "_id": ObjectId(),
                "text": "Which service provides a firewall to control traffic to and from your AWS resources?",
                "type": "multiple_choice",
                "options": ["CloudWatch", "Security Groups", "Route 53", "CloudFront"],
                "correct_answer": "Security Groups",
                "explanation": "Security Groups act as virtual firewalls for EC2 instances to control inbound and outbound traffic."
            }
        ]
    },
    {
        "_id": ObjectId(),
        "title": "Cloud Misconfigurations",
        "description": "Learn about common cloud misconfigurations and how to identify them.",
        "difficulty": "Intermediate",
        "created_at": datetime.datetime.utcnow(),
        "questions": [
            {
                "_id": ObjectId(),
                "text": "Which of the following is considered a critical cloud misconfiguration?",
                "type": "multiple_choice",
                "options": [
                    "Using default names for resources",
                    "Having overly permissive security group rules",
                    "Not tagging resources properly",
                    "Using default VPC settings"
                ],
                "correct_answer": "Having overly permissive security group rules",
                "explanation": "Overly permissive security group rules can expose your resources to unnecessary security risks from the internet."
            },
            {
                "_id": ObjectId(),
                "text": "Storing access keys directly in code is a secure practice.",
                "type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "Storing access keys in code is a security risk as they can be exposed through version control systems or if the code is shared."
            },
            {
                "_id": ObjectId(),
                "text": "Which of the following tools is specialized in detecting cloud misconfigurations?",
                "type": "multiple_choice",
                "options": ["CloudWatch", "Wiz", "CodeDeploy", "CloudFormation"],
                "correct_answer": "Wiz",
                "explanation": "Wiz is a cloud security platform that specializes in detecting misconfigurations and vulnerabilities across multi-cloud environments."
            },
            {
                "_id": ObjectId(),
                "text": "What is an attack path in cloud security?",
                "type": "multiple_choice",
                "options": [
                    "A type of DDoS attack",
                    "A series of connected misconfigurations that could lead to a security breach",
                    "A direct network connection to cloud resources",
                    "A type of malware designed for cloud environments"
                ],
                "correct_answer": "A series of connected misconfigurations that could lead to a security breach",
                "explanation": "Attack paths represent how an attacker could chain together multiple small vulnerabilities to compromise critical assets."
            },
            {
                "_id": ObjectId(),
                "text": "Which practice helps reduce the risk of credential exposure in cloud environments?",
                "type": "multiple_choice",
                "options": [
                    "Using long-lived access keys",
                    "Implementing Just-in-Time (JIT) access",
                    "Sharing credentials among team members",
                    "Storing credentials in environment variables"
                ],
                "correct_answer": "Implementing Just-in-Time (JIT) access",
                "explanation": "JIT access provides temporary, time-limited access to resources only when needed, reducing the risk of credential exposure."
            }
        ]
    }
]

# Create indexes
db.users.create_index("username", unique=True)
db.users.create_index("email", unique=True)

# Clear existing collections and insert new data
db.quizzes.delete_many({})
db.quizzes.insert_many(quizzes)

print(f"Database initialized with {len(quizzes)} quizzes!")
