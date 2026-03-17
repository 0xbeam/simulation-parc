"""
Custom Domain Adapter - Build a domain from a user-provided JSON specification.
"""

from typing import List, Dict, Any

from .base import (
    SimulationAdapter,
    DomainConfig,
    EntityType,
    PlatformType,
    ActionType,
)


class CustomAdapter(SimulationAdapter):
    """Adapter that constructs a DomainConfig from a user-supplied dict/JSON spec.

    Expected spec format::

        {
            "name": "my_domain",
            "display_name": "My Domain",
            "description": "...",
            "entity_types": [
                {"name": "Agent", "description": "..."}
            ],
            "platforms": [
                {
                    "name": "PlatformA",
                    "description": "...",
                    "actions": [
                        {"name": "ACT", "description": "..."}
                    ]
                }
            ],
            "default_max_rounds": 10,
            "default_round_minutes": 60,
            "ontology_prompt_context": "...",
            "profile_prompt_context": "...",
            "report_prompt_context": "..."
        }
    """

    def __init__(self, spec: Dict[str, Any] | None = None):
        if spec is None:
            spec = {}
        self._spec = spec
        self._config = self._build_config(spec)

    @staticmethod
    def _build_config(spec: Dict[str, Any]) -> DomainConfig:
        entity_types = [
            EntityType(name=e["name"], description=e.get("description", ""))
            for e in spec.get("entity_types", [])
        ]

        platforms = []
        for p in spec.get("platforms", []):
            actions = [
                ActionType(
                    name=a["name"],
                    description=a.get("description", ""),
                    platform=p["name"],
                )
                for a in p.get("actions", [])
            ]
            platforms.append(
                PlatformType(
                    name=p["name"],
                    description=p.get("description", ""),
                    actions=actions,
                )
            )

        return DomainConfig(
            name=spec.get("name", "custom"),
            display_name=spec.get("display_name", "Custom Domain"),
            description=spec.get("description", "A user-defined simulation domain."),
            entity_types=entity_types,
            platforms=platforms,
            default_max_rounds=spec.get("default_max_rounds", 10),
            default_round_minutes=spec.get("default_round_minutes", 60),
            ontology_prompt_context=spec.get("ontology_prompt_context", ""),
            profile_prompt_context=spec.get("profile_prompt_context", ""),
            report_prompt_context=spec.get("report_prompt_context", ""),
        )

    def get_config(self) -> DomainConfig:
        return self._config

    def get_profile_schema(self) -> Dict[str, Any]:
        """Return a generic profile schema; users can override via the spec."""
        return self._spec.get("profile_schema", {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Agent name"},
                "role": {"type": "string", "description": "Agent role"},
                "description": {"type": "string", "description": "Agent description"},
            },
            "required": ["name"],
        })

    def get_environment_schema(self) -> Dict[str, Any]:
        """Return a generic environment schema; users can override via the spec."""
        platform_names = [p.name for p in self._config.platforms]
        return self._spec.get("environment_schema", {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": platform_names,
                    "description": "Which platform to simulate",
                },
                "max_rounds": {"type": "integer", "minimum": 1, "description": "Maximum simulation rounds"},
                "round_minutes": {"type": "integer", "minimum": 1, "description": "Simulated minutes per round"},
                "actions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Allowed agent actions",
                },
            },
            "required": ["platform"] if platform_names else [],
        })

    def validate_config(self, config: dict) -> List[str]:
        errors = []
        platform_names = {p.name for p in self._config.platforms}
        platform = config.get("platform")
        if platform and platform_names and platform not in platform_names:
            errors.append(
                f"Unknown platform: {platform}. Must be one of: {', '.join(sorted(platform_names))}."
            )

        if platform:
            valid_actions = set()
            for p in self._config.platforms:
                if p.name == platform:
                    valid_actions = {a.name for a in p.actions}
                    break
            for action in config.get("actions", []):
                if action not in valid_actions:
                    errors.append(f"Invalid action '{action}' for platform '{platform}'.")

        return errors
