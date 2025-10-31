
from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.types import DatabaseConfig, ServerConfig, LoggingConfig

class APIConfig(BaseConfig):
  database: DatabaseConfig
  server: ServerConfig
  logging: LoggingConfig

class APIConfigLoader(ConfigLoader):
  config_class = APIConfig
  prefix = "API"
