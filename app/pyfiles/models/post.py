from app import db
from datetime import datetime


class Post(db.Model):
    """Model for user"""
    post_id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Text, default='{}')
    author = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def get_info(self):
        # return {'username': self.username, 'last_request': self.last_request.strftime('%m/%d/%Y, %H:%M:%S')}
        return {
            'post_id': self.post_id,
            'header': self.header,
            'content': self.content,
            'author': self.author,
            'date': self.date,
            'likes': self.likes,
        }

    def __repr__(self):
        return '<Post %r>' % self.post_id

    # b = list(map(int ,a[1: -1].split(', ')))
    