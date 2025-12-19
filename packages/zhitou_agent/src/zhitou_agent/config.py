from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config.models import DashsopeConfig


class AgentConfig(BaseConfig):
  dashscpope: DashsopeConfig


class AgentConfigLoader(ConfigLoader[AgentConfig]):
  config_class = AgentConfig
  prefix = "agent"
