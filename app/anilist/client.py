import requests
from flask import current_app
import json


def execute_query(query, variables=None):
    """Execute a GraphQL query against the AniList API"""
    url = current_app.config['ANILIST_API_URL']

    response = requests.post(
        url,
        json={'query': query, 'variables': variables}
    )

    if response.status_code == 200:
        return response.json()
    else:
        current_app.logger.error(f"AniList API error: {response.status_code} - {response.text}")
        return None


def search_anime(search_query, genre='', sort='POPULARITY_DESC'):
    """Search for anime by name or genre"""
    query = '''
    query ($search: String, $genre: String, $sort: [MediaSort]) {
        Page(page: 1, perPage: 20) {
            media(type: ANIME, search: $search, genre: $genre, sort: $sort) {
                id
                title {
                    romaji
                    english
                }
                genres
                description
                coverImage {
                    large
                }
                popularity
                averageScore
            }
        }
    }
    '''

    variables = {
        'search': search_query if search_query else None,
        'genre': genre if genre else None,
        'sort': [sort]
    }

    result = execute_query(query, variables)

    if result and 'data' in result and 'Page' in result['data']:
        return result['data']['Page']['media']

    return []


def get_anime_details(anime_id):
    """Get detailed information about a specific anime"""
    query = '''
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            description
            genres
            episodes
            status
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            season
            duration
            coverImage {
                large
            }
            bannerImage
            averageScore
            popularity
            studios {
                nodes {
                    name
                }
            }
        }
    }
    '''

    variables = {
        'id': anime_id
    }

    result = execute_query(query, variables)

    if result and 'data' in result and 'Media' in result['data']:
        return result['data']['Media']

    return None


def get_popular_anime(limit=20):
    """Get popular anime sorted by popularity"""
    query = '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(type: ANIME, sort: POPULARITY_DESC) {
                    id
                    title {
                        romaji
                        english
                    }
                    genres
                    description
                    coverImage {
                        large
                    }
                    popularity
                    averageScore
                }
            }
        }
        '''

    variables = {
        'page': 1,
        'perPage': limit
    }

    result = execute_query(query, variables)

    if result and 'data' in result and 'Page' in result['data']:
        return result['data']['Page']['media']

    return []


def get_anime_by_genre(genre, limit=20):
    """Get anime by genre"""
    query = '''
        query ($genre: String, $page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(type: ANIME, genre: $genre, sort: POPULARITY_DESC) {
                    id
                    title {
                        romaji
                        english
                    }
                    genres
                    description
                    coverImage {
                        large
                    }
                    popularity
                    averageScore
                }
            }
        }
        '''

    variables = {
        'genre': genre,
        'page': 1,
        'perPage': limit
    }

    result = execute_query(query, variables)

    if result and 'data' in result and 'Page' in result['data']:
        return result['data']['Page']['media']

    return []