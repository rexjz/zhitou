from pydantic import BaseModel, Field


class CurrentUserResponseData(BaseModel):
  """Response model for current user information"""

  id: str = Field(..., description="User ID")
  username: str = Field(..., description="Username")
  email: str = Field(..., description="User email address")
