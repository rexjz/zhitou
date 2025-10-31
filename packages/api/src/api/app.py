import os
from api.config import APIConfigLoader, APIConfig
from core.config.types import LoggingConfig
from database.db_manager import DatabaseManager
from loguru import logger
import pathlib
from api.handlers import app
from .state import (
  init_app_state,
  set_request_state,
  get_app_state,
  get_request_state,
  RequestState,
  AppState,
)
import json


def _config_logger(config: LoggingConfig):
  os.makedirs(config.log_file_dir, exist_ok=True)
  logger.add(
    pathlib.Path(config.log_file_dir) / "api.log",
    rotation=config.rotation,
    backtrace=True,
    format="{time} | {level} | {name}:{function}:{line} - {message}",
  )


@app.before_request
def _setup_state():
  app_state = get_app_state()
  set_request_state(RequestState(db_session=app_state.db_manager.get_session()))


@app.teardown_request
def _teardown_state(exc):
  st = get_request_state()
  st.db_session.close()


@logger.catch()
def main():
  loader = APIConfigLoader()
  config: APIConfig = loader.load()
  _config_logger(config.logging)

  logger.debug(f"config loaded:\n {json.dumps(config.model_dump(), indent=2)}")
  with app.app_context():
    # db
    db_manager = DatabaseManager()
    db_manager.init(config.database.url)    
    init_app_state(app, AppState(db_manager=db_manager))
    
    if config.server.dev:
      app.run(
        debug=config.server.debug, host=config.server.host, port=config.server.port
      )
    else:
      from waitress import serve

      logger.info("waitress start serving in production mode")
      serve(app, host=config.server.host, port=config.server.port)


if __name__ == "__main__":
  main()
