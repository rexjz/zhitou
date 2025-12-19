from fastapi import APIRouter, Depends
from api.middleware import get_current_user
from core.models.user import UserModel
from api.api_models.api_response import APIResponse
from api.api_models.user import CurrentUserResponseData


user_router = APIRouter(dependencies=[Depends(get_current_user)])

@user_router.get("/me")
def get_current_user_info(
  current_user: UserModel = Depends(get_current_user)
) -> APIResponse[CurrentUserResponseData]:
  """
  Get current authenticated user information.

  Returns:
    User information including id, username, and email
  """
  return APIResponse[CurrentUserResponseData](
    message="",
    data=CurrentUserResponseData(
      id=current_user.id,
      username=current_user.username,
      email=current_user.username
    )
  )
