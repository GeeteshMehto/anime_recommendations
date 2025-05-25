from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.user.models import UserPreference
from app.user import user_bp
from sqlalchemy.exc import IntegrityError


@user_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    current_user_id = get_jwt_identity()

    preferences = UserPreference.query.filter_by(user_id=current_user_id).all()

    return jsonify({
        'preferences': [pref.to_dict() for pref in preferences]
    })


@user_bp.route('/preferences', methods=['POST'])
@jwt_required()
def add_preference():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if 'genre' not in data:
        return jsonify({'error': 'Genre is required'}), 400

    try:
        # Add new preference
        preference = UserPreference(
            user_id=current_user_id,
            genre=data['genre']
        )

        db.session.add(preference)
        db.session.commit()

        return jsonify({
            'message': 'Preference added successfully',
            'preference': preference.to_dict()
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'This genre preference already exists'}), 400


@user_bp.route('/preferences/<int:pref_id>', methods=['DELETE'])
@jwt_required()
def delete_preference(pref_id):
    current_user_id = get_jwt_identity()

    preference = UserPreference.query.filter_by(
        id=pref_id,
        user_id=current_user_id
    ).first()

    if not preference:
        return jsonify({'error': 'Preference not found'}), 404

    db.session.delete(preference)
    db.session.commit()

    return jsonify({'message': 'Preference deleted successfully'})