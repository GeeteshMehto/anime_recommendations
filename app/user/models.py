from app import db
from datetime import datetime


class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    genre = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Make user_id and genre unique together
    __table_args__ = (db.UniqueConstraint('user_id', 'genre', name='_user_genre_uc'),)

    def to_dict(self):
        return {
            'id': self.id,
            'genre': self.genre,
            'created_at': self.created_at.isoformat()
        }