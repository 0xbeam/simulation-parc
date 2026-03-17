"""
Supply Chain Domain Adapter - Supply chain and logistics simulation.
"""

from typing import List, Dict, Any

from .base import (
    SimulationAdapter,
    DomainConfig,
    EntityType,
    PlatformType,
    ActionType,
)


# Supply-chain-specific action definitions
PROCUREMENT_ACTIONS = [
    "ORDER", "NEGOTIATE", "APPROVE", "REJECT", "REQUEST_QUOTE",
    "AWARD_CONTRACT", "INSPECT", "DO_NOTHING",
]

LOGISTICS_ACTIONS = [
    "SHIP", "RECEIVE", "TRACK", "REROUTE", "WAREHOUSE",
    "DELIVER", "RETURN", "DO_NOTHING",
]


class SupplyChainAdapter(SimulationAdapter):
    """Adapter for supply chain and logistics simulation."""

    def __init__(self):
        procurement_actions = [
            ActionType(name=a, description=self._action_desc("Procurement", a), platform="Procurement")
            for a in PROCUREMENT_ACTIONS
        ]
        logistics_actions = [
            ActionType(name=a, description=self._action_desc("Logistics", a), platform="Logistics")
            for a in LOGISTICS_ACTIONS
        ]

        self._config = DomainConfig(
            name="supply_chain",
            display_name="Supply Chain",
            description=(
                "Simulate supply chain dynamics including procurement, logistics, "
                "inventory management, and multi-tier supplier relationships."
            ),
            entity_types=[
                EntityType(name="Supplier", description="A raw material or component supplier"),
                EntityType(name="Manufacturer", description="A manufacturer that assembles products"),
                EntityType(name="Distributor", description="A wholesale distributor"),
                EntityType(name="Retailer", description="An end-point retailer selling to consumers"),
                EntityType(name="Shipment", description="A shipment of goods in transit"),
                EntityType(name="Warehouse", description="A storage facility for inventory"),
            ],
            platforms=[
                PlatformType(
                    name="Procurement",
                    description="Procurement and sourcing platform for ordering, negotiation, and contract management",
                    actions=procurement_actions,
                ),
                PlatformType(
                    name="Logistics",
                    description="Logistics and transportation platform for shipping, tracking, and delivery",
                    actions=logistics_actions,
                ),
            ],
            default_max_rounds=15,
            default_round_minutes=1440,  # 1 day per round
            ontology_prompt_context=(
                "This simulation focuses on supply chain dynamics. "
                "The ontology should capture entities like suppliers, manufacturers, "
                "distributors, retailers, shipments, and warehouses. Relationships include "
                "supplies-to, ships-via, stores-at, and contracts-with. Consider lead times, "
                "inventory levels, demand variability, and disruption propagation."
            ),
            profile_prompt_context=(
                "Generate realistic supply chain participant personas. Each agent should have "
                "a distinct role, capacity constraints, reliability rating, pricing strategy, "
                "geographic location, and risk management approach. Consider tier-1 vs tier-2 "
                "supplier characteristics and regional differences."
            ),
            report_prompt_context=(
                "Analyze the simulation results focusing on supply chain resilience, "
                "bullwhip effect observations, lead time variability, inventory optimization, "
                "bottleneck identification, and cost-efficiency across the network."
            ),
        )

    @staticmethod
    def _action_desc(platform: str, action: str) -> str:
        descriptions = {
            ("Procurement", "ORDER"): "Place a purchase order with a supplier",
            ("Procurement", "NEGOTIATE"): "Negotiate terms, price, or delivery schedule",
            ("Procurement", "APPROVE"): "Approve a pending order or contract",
            ("Procurement", "REJECT"): "Reject a proposal or shipment",
            ("Procurement", "REQUEST_QUOTE"): "Request a price quote from a supplier",
            ("Procurement", "AWARD_CONTRACT"): "Award a procurement contract",
            ("Procurement", "INSPECT"): "Inspect received goods for quality",
            ("Procurement", "DO_NOTHING"): "Take no action this round",
            ("Logistics", "SHIP"): "Ship goods from one location to another",
            ("Logistics", "RECEIVE"): "Receive an incoming shipment",
            ("Logistics", "TRACK"): "Track the status of a shipment",
            ("Logistics", "REROUTE"): "Reroute a shipment to a different destination",
            ("Logistics", "WAREHOUSE"): "Store goods in a warehouse",
            ("Logistics", "DELIVER"): "Complete final delivery to destination",
            ("Logistics", "RETURN"): "Return defective or unwanted goods",
            ("Logistics", "DO_NOTHING"): "Take no action this round",
        }
        return descriptions.get((platform, action), f"{action} on {platform}")

    def get_config(self) -> DomainConfig:
        return self._config

    def get_profile_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Organization name"},
                "role": {
                    "type": "string",
                    "enum": ["supplier", "manufacturer", "distributor", "retailer"],
                    "description": "Role in the supply chain",
                },
                "capacity": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Maximum units that can be handled per round",
                },
                "reliability": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Reliability rating (0-1)",
                },
                "location": {"type": "string", "description": "Geographic location or region"},
                "pricing_strategy": {
                    "type": "string",
                    "enum": ["low_cost", "premium", "competitive", "dynamic"],
                    "description": "Pricing approach",
                },
            },
            "required": ["name", "role"],
        }

    def get_environment_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["Procurement", "Logistics"],
                    "description": "Which supply chain platform to simulate",
                },
                "max_rounds": {"type": "integer", "minimum": 1, "description": "Maximum simulation rounds"},
                "round_minutes": {"type": "integer", "minimum": 1, "description": "Simulated minutes per round"},
                "demand_variability": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Demand variability factor (0-1)",
                },
                "disruption_probability": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Probability of supply disruption per round (0-1)",
                },
                "actions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Allowed agent actions",
                },
            },
            "required": ["platform"],
        }

    def validate_config(self, config: dict) -> List[str]:
        errors = []
        platform = config.get("platform")
        if platform and platform not in ("Procurement", "Logistics"):
            errors.append(f"Unknown platform: {platform}. Must be 'Procurement' or 'Logistics'.")

        actions = config.get("actions", [])
        valid = set(PROCUREMENT_ACTIONS if platform == "Procurement" else LOGISTICS_ACTIONS)
        for action in actions:
            if action not in valid:
                errors.append(f"Invalid action '{action}' for platform '{platform}'.")

        return errors
