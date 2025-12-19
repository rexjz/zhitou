from enum import IntEnum


class BizError(Exception):
  def __init__(
    self, code: str, http_status: int, message: str, source: str, details: dict = None
  ):
    self.code = code
    self.http_status = http_status
    self.message = message
    self.source = source
    self.details = details or {}


class BizErrorCode(IntEnum):
  INTERNAL_ERROR = -10000