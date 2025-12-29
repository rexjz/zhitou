from fastapi import APIRouter, Depends
from api.middleware import get_current_user
from core.models.user import UserModel
from api.api_models.api_response import APIResponse
from pydantic import BaseModel, Field
from typing import Optional
from loguru import logger
from uuid import UUID

user_router = APIRouter(dependencies=[Depends(get_current_user)], tags=["User"])


class CurrentUserResponseData(BaseModel):
  """Response model for current user information"""

  id: UUID = Field(..., description="User ID")
  username: str = Field(..., description="Username")
  email: Optional[str] = Field(..., description="User email address")


@user_router.get("/me", operation_id="get current user")
def get_current_user_info(
  current_user: UserModel = Depends(get_current_user),
) -> APIResponse[CurrentUserResponseData]:
  """
  Get current authenticated user information.

  Returns:
    User information including id, username, and email
  """
  logger.info(f"current_user: {current_user}")
  return APIResponse[CurrentUserResponseData](
    message="",
    data=CurrentUserResponseData(
      id=current_user.id, username=current_user.username, email=current_user.email
    ),
  )
