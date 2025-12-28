from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, Field
from dataclasses import dataclass

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
  """Generic API response model"""

  message: str = Field(default="")
  code: int = Field(default=0)
  data: Optional[T] = None

