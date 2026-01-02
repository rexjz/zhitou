from typing import Any, Dict, List, Literal, Protocol, Tuple
from agno.db.base import BaseDb


class AgentRepository(Protocol):
  def get_sessions(
    self,
    user_id: str,
    page_size: int,
    page_number: int,
    sort_order: Literal["desc", "asc"] = "desc",
  ) -> Tuple[List[Dict[str, Any]], int]:
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
  ):
    return self.db.get_sessions(
      user_id=user_id,
      page=page_number,
      limit=page_size,
      sort_by="created_at",
      sort_order=sort_order,
      deserialize=False
    )
