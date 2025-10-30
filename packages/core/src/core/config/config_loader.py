import os
from confz import BaseConfig, FileSource, EnvSource
from dotenv import load_dotenv


class ConfigLoader:
  """通用配置加载抽象类。"""

  # 子类应重写这两个属性
  prefix: str = ""  # 环境变量前缀
  config_class: type[BaseConfig] = None  # 对应的配置模型（必须是 BaseConfig 子类）

  def __init__(self):
    if not self.config_class:
      raise ValueError("config_class is required")
    if not issubclass(self.config_class, BaseConfig):
      raise TypeError("config_class must be child of confz.BaseConfig")

  def load(self):
    load_dotenv()
    env = os.getenv("ENV", "dev")
    default_config_file = "config/config.default.yaml"
    env_specific_config_file = f"config/config.{env}.yaml"

    print(f"🔧 Loading {self.config_class.__name__} in environment: {env}")

    self.config_class.CONFIG_SOURCES = [
      FileSource(file=default_config_file),
      FileSource(file=env_specific_config_file),
      EnvSource(allow_all=True, prefix=f"{self.prefix}__", nested_separator="__"),
    ]

    return self.config_class()
