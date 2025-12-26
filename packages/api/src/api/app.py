import os
import sys
import uuid
import pathlib
from api.api_models.api_response import APIResponse
from api.config import APIConfigLoader, APIConfig
from contextlib import asynccontextmanager
from api.services.agent.agent_memory_service import AgentMemoryService
from api.services.agent.agent_memory_service_fs_impl import AgentMemoryServiceFSImpl
from core.config.models import LoggingConfig
from core.db_manager import DatabaseManager
from core.error.biz_error import BizError, BizErrorCode
from core.repos.user_repo import UserRepositoryImpl
from api.services.user import UserServiceImpl
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger
from api.handlers.auth import auth_router
from api.handlers.user import user_router
from api.handlers.system import system_router

from typing import cast

import uvicorn
from .state import (
  AgentService,
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
    serialize=True
  )
  # logger.add(sys.stdout, serialize=True)
  # logger.add(sys.stderr, serialize=True)


def init_repositories_state() -> RepositoriesState:
  return RepositoriesState(user_repo=UserRepositoryImpl())


@asynccontextmanager
async def lifespan(app: FastAPI):
  loader = APIConfigLoader()
  config: APIConfig = loader.load()
  _config_logger(config.logging)

  logger.debug(f"config loaded:\n {json.dumps(config.model_dump(), indent=2)}")
  db_manager = DatabaseManager()
  db_manager.init(config.database.url)
  
  repositories = init_repositories_state()
  services = ServicesState(
    user_service=UserServiceImpl(user_repo=repositories.user_repo),
    agent_service=AgentService(
      memory=AgentMemoryServiceFSImpl(base_dir=config.agent.memory_base_dir)
    )
  )
  app.state.state = AppState(
    config=config, db_manager=db_manager, repositories=repositories, services=services
  )
  yield
  # 清理资源


app = FastAPI(lifespan=lifespan)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content=APIResponse(code=BizErrorCode.INTERNAL_ERROR, message=exc.detail),
  )


@app.exception_handler(BizError)
async def handle_biz_error(request: Request, exc: BizError):
  return JSONResponse(
    status_code=exc.http_status,
    content=APIResponse(
      code=exc.code,
      message=exc.message,
    ),
  )


app.include_router(system_router)
app.include_router(auth_router, prefix="/auth")
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
