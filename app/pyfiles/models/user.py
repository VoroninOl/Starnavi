from app import db
from datetime import datetime


class User(db.Model):
    """Model for user"""
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    last_request = db.Column(db.DateTime, default=datetime.utcnow)

    def get_info(self):
        # return {'username': self.username, 'last_request': self.last_request.strftime('%m/%d/%Y, %H:%M:%S')}
        return {'user_id': self.user_id, 'username': self.username,
                'last_request': self.last_request.strftime('%m/%d/%Y, %H:%M:%S')}

    def __repr__(self):
        return '<User %r>' % self.user_id
