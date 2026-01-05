from typing import Any, List, Literal, Protocol, Tuple, TypedDict
from agno.db.base import BaseDb


class ModelData(TypedDict):
  id: str
  name: str
  provider: str


class AgentData(TypedDict):
  name: str
  model: ModelData
  agent_id: str


class SessionData(TypedDict):
  session_id: str
  session_type: str
  agent_id: str
  team_id: str | None
  workflow_id: str | None
  user_id: str
  agent_data: AgentData | None
  team_data: Any | None
  workflow_data: Any | None
  metadata: Any | None
  summary: str | None
  created_at: int
  updated_at: int


class AgentRepository(Protocol):
  def get_sessions(
    self,
    user_id: str,
    page_size: int,
    page_number: int,
    sort_order: Literal["desc", "asc"] = "desc",
  ) -> Tuple[List[SessionData], int]:
    pass


class AgentRepositoryImpl(AgentRepository):
  pass

  def __init__(self, db: BaseDb):
    super().__init__()
    self.db = db

  def get_sessions(
    self,
    user_id: str,
    page_size: int,
    page_number: int,
    sort_order: Literal["desc", "asc"] = "desc",
  ) -> Tuple[List[SessionData], int]:
    return self.db.get_sessions(
      user_id=user_id,
      page=page_number,
      limit=page_size,
      sort_by="created_at",
      sort_order=sort_order,
      deserialize=False
    )
