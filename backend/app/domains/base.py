"""
Domain Abstraction Layer - Core abstractions for multi-domain simulation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class EntityType:
    name: str
    description: str


@dataclass
class ActionType:
    name: str
    description: str
    platform: str  # which platform this action belongs to


@dataclass
class PlatformType:
    name: str
    description: str
    actions: List[ActionType] = field(default_factory=list)


@dataclass
class DomainConfig:
    name: str
    display_name: str
    description: str
    entity_types: List[EntityType] = field(default_factory=list)
    platforms: List[PlatformType] = field(default_factory=list)
    default_max_rounds: int = 10
    default_round_minutes: int = 60
    ontology_prompt_context: str = ""  # Extra context for ontology generation
    profile_prompt_context: str = ""   # Extra context for profile generation
    report_prompt_context: str = ""    # Extra context for report generation


class SimulationAdapter(ABC):
    @abstractmethod
    def get_config(self) -> DomainConfig:
        ...

    @abstractmethod
    def get_profile_schema(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_environment_schema(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def validate_config(self, config: dict) -> List[str]:
        ...
