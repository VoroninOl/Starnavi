from datetime import datetime

from app import db
from app.pyfiles.models.user import User


def update_user_last_request(username):
    """Function to update last activity of user"""
    user = User.query.filter_by(username=username).first()
    user.last_request = datetime.utcnow()
    try:
        db.session.commit()
    except:
        return False
    return True
