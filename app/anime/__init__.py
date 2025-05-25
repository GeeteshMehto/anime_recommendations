from flask import Blueprint

anime_bp = Blueprint('anime', __name__)

from app.anime import routes