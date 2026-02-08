from pydantic_settings import BaseSettings
from typing import Optional


class MCPConfig(BaseSettings):
    """
    Configuration for MCP server.
    Loads settings from environment variables.
    """
    server_host: str = "127.0.0.1"
    server_port: int = 8001
    debug: bool = False

    # Database connection (shared with main backend)
    database_url: str

    # Authentication settings
    require_auth: bool = True

    class Config:
        env_prefix = "MCP_"


# Global instance
mcp_config = MCPConfig()