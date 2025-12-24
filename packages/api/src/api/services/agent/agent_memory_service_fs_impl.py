from api.services.agent.agent_memory_service import AgentMemoryService
from agentscope.memory import MemoryBase
import json
import os

from zhitou_agent.memory.TruncatableMemory import TruncatableMemory


class AgentMemoryServiceFSImpl(AgentMemoryService):
  def __init__(self, base_dir: str):
    super().__init__()
    self.base_dir = base_dir
    os.makedirs(self.base_dir, exist_ok=True)

  def save_memory(self, session_id: str, memory: MemoryBase):
    state = memory.state_dict()
    file_path = os.path.join(self.base_dir, f"{session_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
      json.dump(state, f, ensure_ascii=False)

  def load_memory(self, session_id: str) -> MemoryBase:
    file_path = os.path.join(self.base_dir, f"{session_id}.json")
    memory = TruncatableMemory(max_len=30)
    if os.path.exists(file_path):
      with open(file_path, "r", encoding="utf-8") as f:
        state = json.load(f)
      memory.load_state_dict(state)

    return memory
