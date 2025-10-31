# state.py
from dataclasses import dataclass
from typing import cast
from database.db_manager import DatabaseManager
from flask import Flask, g, current_app
from sqlalchemy.orm import Session

_REQUEST_STATE_KEY = "_request_state"
_APP_STATE_KEY = "_app_state"

@dataclass
class AppState():
  db_manager: DatabaseManager

@dataclass
class RequestState():
  request_id: str
  db_session: Session


def set_request_state(state: RequestState) -> None:
  setattr(g, _REQUEST_STATE_KEY, state)


def get_request_state() -> RequestState:
  state = getattr(g, _REQUEST_STATE_KEY, None)
  if state is None:
    raise RuntimeError("RequestState not initialized")
  return cast(RequestState, state)


def init_app_state(app: Flask, state: AppState):
  app.extensions[_APP_STATE_KEY] = state

def get_app_state() -> AppState:
  state = current_app.extensions.get(_APP_STATE_KEY, None)
  if state is None:
    raise RuntimeError("AppState not initialized")
  return cast(AppState, state)
