"""
Market Domain Adapter - Financial market simulation.
"""

from typing import List, Dict, Any

from .base import (
    SimulationAdapter,
    DomainConfig,
    EntityType,
    PlatformType,
    ActionType,
)


# Market-specific action definitions
EXCHANGE_ACTIONS = [
    "BUY", "SELL", "HOLD", "PLACE_ORDER", "CANCEL_ORDER",
    "MARKET_WATCH", "SET_LIMIT", "SET_STOP_LOSS", "DO_NOTHING",
]

OTC_ACTIONS = [
    "NEGOTIATE", "ACCEPT_OFFER", "REJECT_OFFER", "COUNTER_OFFER",
    "PLACE_ORDER", "CANCEL_ORDER", "DO_NOTHING",
]


class MarketAdapter(SimulationAdapter):
    """Adapter for financial market simulation."""

    def __init__(self):
        exchange_actions = [
            ActionType(name=a, description=self._action_desc("Exchange", a), platform="Exchange")
            for a in EXCHANGE_ACTIONS
        ]
        otc_actions = [
            ActionType(name=a, description=self._action_desc("OTC", a), platform="OTC")
            for a in OTC_ACTIONS
        ]

        self._config = DomainConfig(
            name="market",
            display_name="Financial Market",
            description=(
                "Simulate financial market dynamics including trading strategies, "
                "price discovery, and regulatory impacts across exchanges and OTC markets."
            ),
            entity_types=[
                EntityType(name="Trader", description="An individual or algorithmic trader"),
                EntityType(name="Fund", description="An investment fund or institutional investor"),
                EntityType(name="Exchange", description="A trading venue or marketplace"),
                EntityType(name="Regulator", description="A regulatory body overseeing market activity"),
                EntityType(name="Asset", description="A tradeable financial instrument"),
                EntityType(name="Order", description="A buy or sell order placed by a trader"),
            ],
            platforms=[
                PlatformType(
                    name="Exchange",
                    description="Centralized exchange with order books, limit orders, and market orders",
                    actions=exchange_actions,
                ),
                PlatformType(
                    name="OTC",
                    description="Over-the-counter market with bilateral negotiation and block trades",
                    actions=otc_actions,
                ),
            ],
            default_max_rounds=20,
            default_round_minutes=15,
            ontology_prompt_context=(
                "This simulation focuses on financial market dynamics. "
                "The ontology should capture entities like traders, funds, assets, "
                "orders, exchanges, and regulators. Relationships include trades-with, "
                "holds-position, regulates, and price-influences. Consider market "
                "microstructure, order flow, volatility, and information asymmetry."
            ),
            profile_prompt_context=(
                "Generate realistic market participant personas. Each agent should have "
                "a distinct trading strategy (value, momentum, market-making, etc.), "
                "risk tolerance, capital allocation, time horizon, and information "
                "advantage level. Consider institutional vs retail characteristics."
            ),
            report_prompt_context=(
                "Analyze the simulation results focusing on price discovery efficiency, "
                "market volatility patterns, order flow imbalances, liquidity dynamics, "
                "and the impact of different trading strategies on market stability."
            ),
        )

    @staticmethod
    def _action_desc(platform: str, action: str) -> str:
        descriptions = {
            ("Exchange", "BUY"): "Execute a market buy order",
            ("Exchange", "SELL"): "Execute a market sell order",
            ("Exchange", "HOLD"): "Maintain current positions without trading",
            ("Exchange", "PLACE_ORDER"): "Place a new limit order on the book",
            ("Exchange", "CANCEL_ORDER"): "Cancel an existing open order",
            ("Exchange", "MARKET_WATCH"): "Monitor market data and price movements",
            ("Exchange", "SET_LIMIT"): "Set a limit price for an order",
            ("Exchange", "SET_STOP_LOSS"): "Set a stop-loss trigger price",
            ("Exchange", "DO_NOTHING"): "Take no action this round",
            ("OTC", "NEGOTIATE"): "Initiate a bilateral negotiation",
            ("OTC", "ACCEPT_OFFER"): "Accept a counterparty's offer",
            ("OTC", "REJECT_OFFER"): "Reject a counterparty's offer",
            ("OTC", "COUNTER_OFFER"): "Submit a counter-proposal",
            ("OTC", "PLACE_ORDER"): "Place an OTC order",
            ("OTC", "CANCEL_ORDER"): "Cancel an OTC order",
            ("OTC", "DO_NOTHING"): "Take no action this round",
        }
        return descriptions.get((platform, action), f"{action} on {platform}")

    def get_config(self) -> DomainConfig:
        return self._config

    def get_profile_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Trader or fund name"},
                "strategy": {
                    "type": "string",
                    "enum": ["value", "momentum", "market_making", "arbitrage", "passive", "aggressive"],
                    "description": "Primary trading strategy",
                },
                "risk_tolerance": {
                    "type": "string",
                    "enum": ["conservative", "moderate", "aggressive"],
                    "description": "Risk appetite level",
                },
                "capital": {
                    "type": "number",
                    "minimum": 0,
                    "description": "Starting capital allocation",
                },
                "time_horizon": {
                    "type": "string",
                    "enum": ["short_term", "medium_term", "long_term"],
                    "description": "Investment time horizon",
                },
                "information_level": {
                    "type": "string",
                    "enum": ["retail", "informed", "insider"],
                    "description": "Information advantage level",
                },
            },
            "required": ["name", "strategy", "risk_tolerance"],
        }

    def get_environment_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["Exchange", "OTC"],
                    "description": "Which market venue to simulate",
                },
                "max_rounds": {"type": "integer", "minimum": 1, "description": "Maximum simulation rounds"},
                "round_minutes": {"type": "integer", "minimum": 1, "description": "Simulated minutes per round"},
                "initial_price": {"type": "number", "minimum": 0, "description": "Initial asset price"},
                "volatility": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Market volatility parameter (0-1)",
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
        if platform and platform not in ("Exchange", "OTC"):
            errors.append(f"Unknown platform: {platform}. Must be 'Exchange' or 'OTC'.")

        actions = config.get("actions", [])
        valid = set(EXCHANGE_ACTIONS if platform == "Exchange" else OTC_ACTIONS)
        for action in actions:
            if action not in valid:
                errors.append(f"Invalid action '{action}' for platform '{platform}'.")

        return errors
