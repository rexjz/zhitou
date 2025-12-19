from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config import DashsopeConfig, BochaConfig


class AgentConfig(BaseConfig):
  dashscpope: DashsopeConfig
  bocha: BochaConfig

class AgentConfigLoader(ConfigLoader[AgentConfig]):
  config_class = AgentConfig
  prefix = "agent"
