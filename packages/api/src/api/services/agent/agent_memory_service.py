from agentscope.memory import MemoryBase
from typing import Protocol


class AgentMemoryService(Protocol):
  def save_memory(session_id: str, memory: MemoryBase):
    pass

  def load_memory(session_id: str) -> MemoryBase:
    pass
