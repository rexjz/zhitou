# state.py
from dataclasses import dataclass
from typing import cast
from core.db_manager import DatabaseManager
from core.repos.user_repo import UserRepository
from fastapi import Request
from sqlalchemy.orm import Session
from api.config import APIConfig

@dataclass
class RepositoriesState:
  user_repo: UserRepository


@dataclass
class AppState:
  config: APIConfig
  db_manager: DatabaseManager
  repositories: RepositoriesState


@dataclass
class RequestState:
  request_id: str
  db_session: Session


def get_app_state_dep(request: Request) -> AppState:
  return cast(AppState, request.app.state.state)

def get_request_state_dep(request: Request) -> AppState:
  return cast(RequestState, request.state.state)
