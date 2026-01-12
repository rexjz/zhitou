# state.py
from dataclasses import dataclass
from typing import cast, Optional
from core.db_manager import DatabaseManager
from core.repos.user_repo import UserRepository
from core.repos.company_repo import CompanyRepository
from core.repos.report_file_repo import AnnouncementFileRepository
from core.models.user import UserModel
from api.services.user import UserService
from api.services.company import CompanyService
from api.services.report_file import ReportFileService
from fastapi import Request
from sqlalchemy.orm import Session
from api.config import APIConfig
from zhitou_agent.memory.agent_repo import AgentRepository

@dataclass
class RepositoriesState:
  user_repo: UserRepository
  agent_repo: AgentRepository
  company_repo: CompanyRepository
  report_file_repo: AnnouncementFileRepository


@dataclass
class ServicesState:
  user_service: UserService
  company_service: CompanyService
  report_file_service: ReportFileService


@dataclass
class AppState:
  config: APIConfig
  db_manager: DatabaseManager
  repositories: RepositoriesState
  services: ServicesState


@dataclass
class RequestState:
  request_id: str
  db_session: Session
  user: Optional["UserModel"] = None


def get_app_state_dep(request: Request) -> AppState:
  return cast(AppState, request.app.state.state)

def get_request_state_dep(request: Request) -> AppState:
  return cast(RequestState, request.state.r_state)
