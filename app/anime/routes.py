from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.anilist.client import search_anime, get_anime_details
from app.anime.models import WatchedAnime, CachedAnime
from app.user.models import UserPreference
from app.anime import anime_bp


@anime_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    genre = request.args.get('genre', '')

    if not query and not genre:
        return jsonify({'error': 'Please provide a search query or genre'}), 400

    # Search anime using AniList API
    results = search_anime(query, genre)

    # Cache results in the database
    for anime in results:
        existing = CachedAnime.query.filter_by(anilist_id=anime['id']).first()
        if not existing:
            genres_str = ','.join(anime.get('genres', []))
            new_cache = CachedAnime(
                anilist_id=anime['id'],
                title=anime['title']['romaji'],
                genres=genres_str,
                description=anime.get('description', ''),
                image_url=anime.get('coverImage', {}).get('large', ''),
                popularity=anime.get('popularity', 0),
                average_score=anime.get('averageScore', 0)
            )
            db.session.add(new_cache)

    db.session.commit()

    return jsonify({'results': results})


@anime_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def recommendations():
    current_user_id = get_jwt_identity()

    # Get user preferences
    user_preferences = UserPreference.query.filter_by(user_id=current_user_id).all()
    preferred_genres = [pref.genre for pref in user_preferences]

    # Get watched anime
    watched = WatchedAnime.query.filter_by(user_id=current_user_id).all()
    watched_anime_ids = [wa.anime_id for wa in watched]

    # Get recommendations based on preferences
    recommendations = []

    # If user has preferences, use them for recommendations
    if preferred_genres:
        for genre in preferred_genres:
            # Search for anime with this genre that user hasn't watched yet
            genre_results = search_anime('', genre)

            for anime in genre_results:
                if anime['id'] not in watched_anime_ids and not any(
                        r.get('id') == anime['id'] for r in recommendations):
                    recommendations.append(anime)

                    # Cache this anime if not already cached
                    existing = CachedAnime.query.filter_by(anilist_id=anime['id']).first()
                    if not existing:
                        genres_str = ','.join(anime.get('genres', []))
                        new_cache = CachedAnime(
                            anilist_id=anime['id'],
                            title=anime['title']['romaji'],
                            genres=genres_str,
                            description=anime.get('description', ''),
                            image_url=anime.get('coverImage', {}).get('large', ''),
                            popularity=anime.get('popularity', 0),
                            average_score=anime.get('averageScore', 0)
                        )
                        db.session.add(new_cache)
                        db.session.commit()

                # Limit to 10 recommendations
                if len(recommendations) >= 10:
                    break

            if len(recommendations) >= 10:
                break

    # If we don't have enough recommendations, add popular anime
    if len(recommendations) < 10:
        popular_anime = search_anime('', '', sort='POPULARITY_DESC')

        for anime in popular_anime:
            if anime['id'] not in watched_anime_ids and not any(r.get('id') == anime['id'] for r in recommendations):
                recommendations.append(anime)

                # Cache this anime if not already cached
                existing = CachedAnime.query.filter_by(anilist_id=anime['id']).first()
                if not existing:
                    genres_str = ','.join(anime.get('genres', []))
                    new_cache = CachedAnime(
                        anilist_id=anime['id'],
                        title=anime['title']['romaji'],
                        genres=genres_str,
                        description=anime.get('description', ''),
                        image_url=anime.get('coverImage', {}).get('large', ''),
                        popularity=anime.get('popularity', 0),
                        average_score=anime.get('averageScore', 0)
                    )
                    db.session.add(new_cache)
                    db.session.commit()

            # Limit to 10 recommendations
            if len(recommendations) >= 10:
                break

    return jsonify({'recommendations': recommendations[:10]})


@anime_bp.route('/ping', methods=['GET', 'POST'])
def ping():
    print("=== PING ROUTE HIT ===")
    return jsonify({'message': 'Anime blueprint is working', 'method': request.method})

@anime_bp.route('/watched', methods=['POST'])
@jwt_required()
def add_watched():
    print("=== DEBUG START ===")
    print("Content-Type:", request.content_type)
    print("Raw data:", request.data)
    print("Headers:", dict(request.headers))

    # Single JSON validation check
    if not request.is_json:
        print("ERROR: Request is not JSON")
        return jsonify({'error': 'Request content-type must be application/json'}), 415

    # Get JSON data once
    try:
        data = request.get_json()
        print("Parsed JSON data:", data)
    except Exception as e:
        print("JSON parsing error:", str(e))
        return jsonify({'error': 'Invalid JSON format'}), 422

    if not data:
        print("ERROR: Data is None or empty")
        return jsonify({'error': 'Empty JSON body'}), 422

    print("Data type:", type(data))
    print("Data keys:", list(data.keys()) if isinstance(data, dict) else "Not a dict")

    # Validate required fields
    required_fields = ['anime_id', 'anime_title']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        print(f"ERROR: Missing fields: {missing_fields}")
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    print("All required fields present")
    print("=== DEBUG END ===")

    current_user_id = get_jwt_identity()

    # Check if anime is already in watched list
    existing = WatchedAnime.query.filter_by(
        user_id=current_user_id,
        anime_id=data['anime_id']
    ).first()

    if existing:
        # Update existing record
        existing.rating = data.get('rating')
        db.session.commit()
        return jsonify({'message': 'Watched anime updated', 'watched': existing.to_dict()}), 200

    # Add to watched list
    watched = WatchedAnime(
        user_id=current_user_id,
        anime_id=data['anime_id'],
        anime_title=data['anime_title'],
        rating=data.get('rating')
    )

    db.session.add(watched)
    db.session.commit()

    return jsonify({'message': 'Anime added to watched list', 'watched': watched.to_dict()}), 201



@anime_bp.route('/watched', methods=['GET'])
@jwt_required()
def get_watched():
    current_user_id = get_jwt_identity()

    watched_anime = WatchedAnime.query.filter_by(user_id=current_user_id).all()

    return jsonify({'watched_anime': [wa.to_dict() for wa in watched_anime]})


@anime_bp.route('/watched/<int:anime_id>', methods=['DELETE'])
@jwt_required()
def remove_watched(anime_id):
    current_user_id = get_jwt_identity()

    watched = WatchedAnime.query.filter_by(
        user_id=current_user_id,
        anime_id=anime_id
    ).first()

    if not watched:
        return jsonify({'error': 'Anime not found in watched list'}), 404

    db.session.delete(watched)
    db.session.commit()

    return jsonify({'message': 'Anime removed from watched list'})