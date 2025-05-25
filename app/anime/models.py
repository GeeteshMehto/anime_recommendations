from app import db
from datetime import datetime


class WatchedAnime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anime_id = db.Column(db.Integer, nullable=False)
    anime_title = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=True)  # User's rating (1-10)
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'anime_id': self.anime_id,
            'anime_title': self.anime_title,
            'rating': self.rating,
            'watched_at': self.watched_at.isoformat()
        }


class CachedAnime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anilist_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    genres = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    popularity = db.Column(db.Integer, nullable=True)
    average_score = db.Column(db.Float, nullable=True)
    cached_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.anilist_id,
            'title': self.title,
            'genres': self.genres.split(',') if self.genres else [],
            'description': self.description,
            'image_url': self.image_url,
            'popularity': self.popularity,
            'average_score': self.average_score
        }