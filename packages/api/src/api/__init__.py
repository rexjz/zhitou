import os
from api.config import APIConfigLoader, APIConfig
from core.config.types import LoggingConfig
from loguru import logger
import pathlib
from api.handlers import app

def _config_logger(config: LoggingConfig):
  os.makedirs(config.log_file_dir, exist_ok=True)
  logger.add(
    pathlib.Path(config.log_file_dir) / "api.log",
    rotation=config.rotation,
    backtrace=True,
    format="{time} | {level} | {name}:{function}:{line} - {message}",
  )


@logger.catch()
def main():
  loader = APIConfigLoader()
  config: APIConfig = loader.load()
  _config_logger(config.logging)
  if config.server.dev:
    app.run(debug=config.server.debug, host=config.server.host, port=config.server.port)
  else:
    from waitress import serve
    logger.info("waitress start serving in production mode")
    serve(app,  host=config.server.host, port=config.server.port)
    
  
