from agentscope.memory import InMemoryMemory


class TruncatableMemory(InMemoryMemory):
  def __init__(self, max_len: int):
    super().__init__()
    self.max_len = max_len

  def add(self, msg):
    super().add(msg)
    # 保持 buffer 长度 <= max_len
    if len(self._messages) > self.max_len:
      self._messages = self._messages[-self.max_len :]
