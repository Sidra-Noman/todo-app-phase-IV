from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import ConfigDict, field_validator

class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    cors_origins: Union[List[str], str] = ["http://localhost:3000"]
    cohere_api_key: str

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    model_config = ConfigDict(
        env_file=".env",
        extra='ignore'
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        if isinstance(self.cors_origins, str):
            self.cors_origins = [origin.strip() for origin in self.cors_origins.split(',')]

settings = Settings()
