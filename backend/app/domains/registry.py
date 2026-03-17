"""
Domain Registry - Central registry for simulation domain adapters.
"""

from .base import DomainConfig, SimulationAdapter
from typing import Dict, Optional


_registry: Dict[str, SimulationAdapter] = {}


def register_domain(name: str, adapter: SimulationAdapter):
    _registry[name] = adapter


def get_domain(name: str) -> Optional[SimulationAdapter]:
    return _registry.get(name)


def list_domains() -> list:
    return [
        {
            "name": name,
            "display_name": adapter.get_config().display_name,
            "description": adapter.get_config().description,
            "platforms": [p.name for p in adapter.get_config().platforms],
        }
        for name, adapter in _registry.items()
    ]


def get_default_domain() -> str:
    return "social_media"
