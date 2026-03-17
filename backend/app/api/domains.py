"""
Domain API endpoints - List and inspect registered simulation domains.
"""

from dataclasses import asdict
from flask import Blueprint, jsonify

from ..domains.registry import list_domains, get_domain

domains_bp = Blueprint('domains', __name__)


@domains_bp.route('/', methods=['GET'])
def get_domains():
    """GET /api/domains - List all registered simulation domains."""
    return jsonify({
        "success": True,
        "domains": list_domains(),
    })


@domains_bp.route('/<name>', methods=['GET'])
def get_domain_detail(name: str):
    """GET /api/domains/<name> - Get detailed domain config."""
    adapter = get_domain(name)
    if adapter is None:
        return jsonify({"success": False, "error": f"Domain '{name}' not found"}), 404

    config = adapter.get_config()

    # Serialize platforms with their actions
    platforms = []
    for p in config.platforms:
        platforms.append({
            "name": p.name,
            "description": p.description,
            "actions": [
                {"name": a.name, "description": a.description}
                for a in p.actions
            ],
        })

    return jsonify({
        "success": True,
        "domain": {
            "name": config.name,
            "display_name": config.display_name,
            "description": config.description,
            "entity_types": [
                {"name": e.name, "description": e.description}
                for e in config.entity_types
            ],
            "platforms": platforms,
            "default_max_rounds": config.default_max_rounds,
            "default_round_minutes": config.default_round_minutes,
            "profile_schema": adapter.get_profile_schema(),
            "environment_schema": adapter.get_environment_schema(),
        },
    })
