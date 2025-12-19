
from typing import Optional
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
  kb_name: str

class ChinaAnnualReportSoures(BaseModel):
  listing_file_path: str
  base_path: Optional[str]

class JWTConfig(BaseModel):
  secret_key: str
  algorithm: str = Field(default="HS256")
  access_token_expire_minutes: int = Field(default=30)
  cookie_name: str = Field(default="zhitou_access_token")