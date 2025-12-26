
from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.models import ChinaAnnualReportSoures, DatabaseConfig, RAGFlowConfig

class WorkerConfig(BaseConfig):
  database: DatabaseConfig
  ragflow: RAGFlowConfig
  china_annual_report_soures: ChinaAnnualReportSoures
  

class WorkerConfigLoader(ConfigLoader):
  config_class = WorkerConfig
  prefix = "WORKER"
