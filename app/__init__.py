from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, root_path='C:\\Users\\Anthony\\GitWorkspace\\magnetic_test_exercise')
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object('config')
db = SQLAlchemy(app)

from app.resources import bidder
