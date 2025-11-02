
from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.models import DatabaseConfig

class WorkerConfig(BaseConfig):
  database: DatabaseConfig

class WorkerConfigLoader(ConfigLoader):
  config_class = WorkerConfig
  prefix = "API"
