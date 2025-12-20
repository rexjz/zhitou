import os
import pathlib
import sys
from confz import BaseConfig
from core.config.config_loader import ConfigLoader
from core.config import DashsopeConfig, BochaConfig
from core.config.models import LoggingConfig
from loguru import logger


class AgentConfig(BaseConfig):
  dashscpope: DashsopeConfig
  bocha: BochaConfig
  logging: LoggingConfig

class AgentConfigLoader(ConfigLoader[AgentConfig]):
  config_class = AgentConfig
  prefix = "agent"


def config_logger(config: LoggingConfig):
  os.makedirs(config.log_file_dir, exist_ok=True)
  logger.add(
    pathlib.Path(config.log_file_dir) / "agent.log",
    rotation=config.rotation,
    backtrace=True,
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    serialize=True
  )
  logger.add(
    sys.stdout,
    serialize=True
  )
  logger.add(
    sys.stderr,
    serialize=True
  )