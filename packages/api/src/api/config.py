
from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.models import DatabaseConfig, RedisConfig, ServerConfig, LoggingConfig

class APIConfig(BaseConfig):
  database: DatabaseConfig
  server: ServerConfig
  logging: LoggingConfig
  redis: RedisConfig

class APIConfigLoader(ConfigLoader):
  config_class = APIConfig
  prefix = "API"
