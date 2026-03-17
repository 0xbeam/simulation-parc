"""
JWT authentication helpers for MiroFish.

Provides token generation/verification and a Flask before_request hook
that protects all /api/ routes except explicitly whitelisted paths.
"""

import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import request, jsonify, g


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_SECRET_KEY = os.environ.get('SECRET_KEY', 'mirofish-dev-only-key')
_ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
_ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'changeme')
_TOKEN_EXPIRY_HOURS = 24

# Paths that do NOT require authentication
_PUBLIC_PATHS = {'/health', '/api/auth/login'}


# ---------------------------------------------------------------------------
# Token helpers
# ---------------------------------------------------------------------------

def generate_token(user_id: str) -> tuple:
    """Return (token_str, expires_at_iso) for *user_id*."""
    expires_at = datetime.now(timezone.utc) + timedelta(hours=_TOKEN_EXPIRY_HOURS)
    payload = {
        'sub': user_id,
        'iat': datetime.now(timezone.utc),
        'exp': expires_at,
    }
    token = jwt.encode(payload, _SECRET_KEY, algorithm='HS256')
    return token, expires_at.isoformat()


def verify_token(token: str) -> dict | None:
    """Decode and verify *token*. Returns the payload dict or ``None``."""
    try:
        return jwt.decode(token, _SECRET_KEY, algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def check_credentials(username: str, password: str) -> bool:
    """Validate username/password against the configured admin account."""
    return username == _ADMIN_USER and password == _ADMIN_PASSWORD


# ---------------------------------------------------------------------------
# Flask decorator (per-route opt-in)
# ---------------------------------------------------------------------------

def login_required(f):
    """Decorator that enforces JWT auth on a single view function."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'Missing or invalid token'}), 401
        token = auth_header.split(' ', 1)[1]
        payload = verify_token(token)
        if payload is None:
            return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401
        g.current_user = payload.get('sub')
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Global before_request hook
# ---------------------------------------------------------------------------

def login_required_hook():
    """
    A Flask ``before_request`` hook that protects every ``/api/`` route
    except those in ``_PUBLIC_PATHS`` and preflight (OPTIONS) requests.

    Register via ``app.before_request(login_required_hook)``.
    """
    # Always allow OPTIONS (CORS preflight)
    if request.method == 'OPTIONS':
        return None

    # Allow explicitly public paths
    if request.path in _PUBLIC_PATHS:
        return None

    # Only protect /api/ namespace
    if not request.path.startswith('/api/'):
        return None

    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'success': False, 'error': 'Authentication required'}), 401

    token = auth_header.split(' ', 1)[1]
    payload = verify_token(token)
    if payload is None:
        return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401

    # Stash current user on Flask's request-scoped `g` object
    g.current_user = payload.get('sub')
    return None
