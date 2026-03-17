"""
Authentication API blueprint.

POST /api/auth/login  - obtain a JWT
GET  /api/auth/me     - return current user info (requires auth)
"""

from flask import Blueprint, request, jsonify, g

from ..auth import generate_token, check_credentials, login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '')
    password = data.get('password', '')

    if not check_credentials(username, password):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    token, expires_at = generate_token(username)
    return jsonify({
        'success': True,
        'token': token,
        'expires_at': expires_at,
        'user': {'username': username},
    })


@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify({
        'success': True,
        'user': {'username': g.current_user},
    })
