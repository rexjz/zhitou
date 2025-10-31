
from pydantic import BaseModel, Field, IPvAnyAddress


class DatabaseConfig(BaseModel):
  url: str

class ServerConfig(BaseModel):
  ip: IPvAnyAddress
  port: int

class LoggingConfig(BaseModel):
  log_file_dir: str
  rotation: str
  log_format: str = Field(default="{time} | {level} | {name}:{function}:{line} - {message}")