# This .py focusses on users and DB connectivity

from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash # Auth/Hashing module, doing hashing in this case
from bson.objectid import ObjectId
import datetime
