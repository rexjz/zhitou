import os
import uuid
import pathlib
from api.api_models.api_response import APIResponse
from api.config import APIConfigLoader, APIConfig
from contextlib import asynccontextmanager
from core.config.models import LoggingConfig
from core.db_manager import DatabaseManager
from core.repos.user_repo import UserRepositoryImpl
from api.services.user import UserServiceImpl
from fastapi import FastAPI, Request
from loguru import logger
from api.handlers.user import user_router
from api.middleware import JWTAuthMiddleware

from typing import cast

import uvicorn
from .state import (
  RepositoriesState,
  ServicesState,
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


def init_repositories_state() -> RepositoriesState:
  return RepositoriesState(user_repo=UserRepositoryImpl())


def init_services_state(repositories: RepositoriesState) -> ServicesState:
  return ServicesState(
    user_service=UserServiceImpl(user_repo=repositories.user_repo)
  )


@asynccontextmanager
async def lifespan(app: FastAPI):
  loader = APIConfigLoader()
  config: APIConfig = loader.load()
  _config_logger(config.logging)

  logger.debug(f"config loaded:\n {json.dumps(config.model_dump(), indent=2)}")
  db_manager = DatabaseManager()
  db_manager.init(config.database.url)
  repositories = init_repositories_state()
  services = init_services_state(repositories)
  app.state.state = AppState(
    config=config,
    db_manager=db_manager,
    repositories=repositories,
    services=services
  )
  yield
  # 清理资源


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
  return APIResponse(message="ok")


@app.get("/")
def root():
  return "ok"


app.include_router(user_router, prefix="/user")


@app.middleware("http")
async def add_request_state(request: Request, call_next):
  app_state = cast(AppState, request.app.state.state)
  request.state.r_state = RequestState(
    db_session=app_state.db_manager.get_session(), request_id=str(uuid.uuid4())
  )
  response = await call_next(request)
  response.headers["X-Request-ID"] = request.state.r_state.request_id
  return response


# JWT Authentication Middleware
# Exclude paths that don't require authentication
jwt_auth_middleware = JWTAuthMiddleware(
  exclude_paths=["/health", "/", "/user/login", "/user/register"]
)
app.middleware("http")(jwt_auth_middleware)


@logger.catch()
def main():
  loader = APIConfigLoader()
  config: APIConfig = loader.load()
  uvicorn.run(
    "api.app:app",
    host=config.server.host,
    port=config.server.port,
    reload=config.server.reload,
  )


if __name__ == "__main__":
  main()
