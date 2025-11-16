
from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
  url: str
  port: int

class RedisConfig(BaseModel):
  url: str
  port: int

class ServerConfig(BaseModel):
  host: str
  port: int
  reload: bool

class LoggingConfig(BaseModel):
  log_file_dir: str
  rotation: str
  log_format: str = Field(default="{time} | {level} | {name}:{function}:{line} - {message}")

class RAGFlowConfig(BaseModel):
  url: str
  apikey: str
