
from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.types import DatabaseConfig, ServerConfig

class APIConfig(BaseConfig):
  database: DatabaseConfig
  server: ServerConfig

class APIConfigLoader(ConfigLoader):
  config_class = APIConfig
  prefix = "API"
