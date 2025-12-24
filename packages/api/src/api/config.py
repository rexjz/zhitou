
from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.models import AgentConfig, DatabaseConfig, RedisConfig, ServerConfig, LoggingConfig, JWTConfig

class APIConfig(BaseConfig):
  database: DatabaseConfig
  server: ServerConfig
  logging: LoggingConfig
  redis: RedisConfig
  jwt: JWTConfig
  agent: AgentConfig

class APIConfigLoader(ConfigLoader):
  config_class = APIConfig
  prefix = "API"
