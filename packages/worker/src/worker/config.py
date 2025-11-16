
from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.models import DatabaseConfig, RAGFlowConfig

class WorkerConfig(BaseConfig):
  database: DatabaseConfig
  ragflow: RAGFlowConfig
  

class WorkerConfigLoader(ConfigLoader):
  config_class = WorkerConfig
  prefix = "API"
