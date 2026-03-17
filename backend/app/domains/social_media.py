"""
Social Media Domain Adapter - Twitter/Reddit simulation (existing behavior).
"""

from typing import List, Dict, Any

from .base import (
    SimulationAdapter,
    DomainConfig,
    EntityType,
    PlatformType,
    ActionType,
)
from ..config import Config


class SocialMediaAdapter(SimulationAdapter):
    """Adapter for social media opinion dynamics simulation (Twitter & Reddit)."""

    def __init__(self):
        twitter_actions = [
            ActionType(name=a, description=self._action_desc("Twitter", a), platform="Twitter")
            for a in Config.OASIS_TWITTER_ACTIONS
        ]
        reddit_actions = [
            ActionType(name=a, description=self._action_desc("Reddit", a), platform="Reddit")
            for a in Config.OASIS_REDDIT_ACTIONS
        ]

        self._config = DomainConfig(
            name="social_media",
            display_name="Social Media",
            description=(
                "Simulate opinion dynamics and information propagation across "
                "social media platforms such as Twitter and Reddit."
            ),
            entity_types=[
                EntityType(name="User", description="A social media user with a persona and opinions"),
                EntityType(name="Post", description="Content published by a user"),
                EntityType(name="Comment", description="A reply or comment on a post"),
                EntityType(name="Topic", description="A trending topic or hashtag"),
            ],
            platforms=[
                PlatformType(
                    name="Twitter",
                    description="Micro-blogging platform with posts, reposts, likes, and follows",
                    actions=twitter_actions,
                ),
                PlatformType(
                    name="Reddit",
                    description="Forum-style platform with posts, comments, upvotes, and communities",
                    actions=reddit_actions,
                ),
            ],
            default_max_rounds=Config.OASIS_DEFAULT_MAX_ROUNDS,
            default_round_minutes=60,
            ontology_prompt_context=(
                "This simulation focuses on social media opinion dynamics. "
                "The ontology should capture entities like users, posts, comments, "
                "topics, and relationships such as follows, replies-to, mentions, "
                "and opinion-influence. Consider sentiment polarity, engagement "
                "metrics, and information cascade patterns."
            ),
            profile_prompt_context=(
                "Generate realistic social media personas. Each agent should have "
                "a distinct personality, posting style, opinion stance, activity level, "
                "and social influence score. Consider demographics, interests, "
                "and political/social leanings."
            ),
            report_prompt_context=(
                "Analyze the simulation results focusing on opinion shift patterns, "
                "echo chamber formation, information spread velocity, engagement "
                "metrics over rounds, and key influencer identification."
            ),
        )

    @staticmethod
    def _action_desc(platform: str, action: str) -> str:
        """Generate a human-readable description for a platform action."""
        descriptions = {
            # Twitter
            ("Twitter", "CREATE_POST"): "Create a new tweet",
            ("Twitter", "LIKE_POST"): "Like an existing tweet",
            ("Twitter", "REPOST"): "Retweet a post",
            ("Twitter", "FOLLOW"): "Follow another user",
            ("Twitter", "DO_NOTHING"): "Take no action this round",
            ("Twitter", "QUOTE_POST"): "Quote-tweet with commentary",
            # Reddit
            ("Reddit", "LIKE_POST"): "Upvote a post",
            ("Reddit", "DISLIKE_POST"): "Downvote a post",
            ("Reddit", "CREATE_POST"): "Create a new post in a subreddit",
            ("Reddit", "CREATE_COMMENT"): "Comment on a post",
            ("Reddit", "LIKE_COMMENT"): "Upvote a comment",
            ("Reddit", "DISLIKE_COMMENT"): "Downvote a comment",
            ("Reddit", "SEARCH_POSTS"): "Search for posts",
            ("Reddit", "SEARCH_USER"): "Search for a user",
            ("Reddit", "TREND"): "Browse trending content",
            ("Reddit", "REFRESH"): "Refresh the feed",
            ("Reddit", "DO_NOTHING"): "Take no action this round",
            ("Reddit", "FOLLOW"): "Follow a user",
            ("Reddit", "MUTE"): "Mute a user",
        }
        return descriptions.get((platform, action), f"{action} on {platform}")

    def get_config(self) -> DomainConfig:
        return self._config

    def get_profile_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Display name"},
                "bio": {"type": "string", "description": "Profile biography"},
                "personality": {"type": "string", "description": "Personality traits summary"},
                "opinion_stance": {"type": "string", "description": "General opinion stance on simulation topic"},
                "activity_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "How frequently the agent acts",
                },
                "influence_score": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Social influence score (0-1)",
                },
            },
            "required": ["username", "personality", "opinion_stance"],
        }

    def get_environment_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["Twitter", "Reddit"],
                    "description": "Which social media platform to simulate",
                },
                "max_rounds": {"type": "integer", "minimum": 1, "description": "Maximum simulation rounds"},
                "round_minutes": {"type": "integer", "minimum": 1, "description": "Simulated minutes per round"},
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
        if platform and platform not in ("Twitter", "Reddit"):
            errors.append(f"Unknown platform: {platform}. Must be 'Twitter' or 'Reddit'.")

        actions = config.get("actions", [])
        if platform == "Twitter":
            valid = set(Config.OASIS_TWITTER_ACTIONS)
        elif platform == "Reddit":
            valid = set(Config.OASIS_REDDIT_ACTIONS)
        else:
            valid = set()

        for action in actions:
            if action not in valid:
                errors.append(f"Invalid action '{action}' for platform '{platform}'.")

        return errors
