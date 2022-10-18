from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.pyfiles.config import secret

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret

db = SQLAlchemy(app)

from app.pyfiles import routes

