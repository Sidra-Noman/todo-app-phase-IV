from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict
from pathlib import Path


class CohereConfig(BaseSettings):
    """
    Configuration for Cohere API integration.
    Loads settings from environment variables.
    """
    cohere_api_key: str  # This maps to COHERE_API_KEY environment variable
    cohere_model: str = "command-r-plus"  # Default model
    cohere_timeout: int = 30  # Timeout in seconds

    model_config = ConfigDict(
        env_file=".env",  # Look for .env file in the current directory
        extra="ignore"  # Ignore extra environment variables that don't match fields
    )


# Global instance
cohere_config = CohereConfig()