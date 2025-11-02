from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.models import DatabaseConfig, LoggingConfig

class DBMigrationConfig(BaseConfig):
  database: DatabaseConfig
  logging: LoggingConfig

class DBMigrationConfigLoader(ConfigLoader):
  config_class = DBMigrationConfig
  prefix = "database_migration"
