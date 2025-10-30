
from confz import BaseConfig
from pydantic import BaseModel, IPvAnyAddress


class DatabaseConfig(BaseModel):
  url: str

class ServerConfig(BaseConfig):
  ip: IPvAnyAddress
  port: int
