from fastapi import APIRouter
from typing import Annotated
from api.api_models.api_response import APIResponse
from fastapi import Depends
from api.state import get_app_state_dep, get_request_state_dep, AppState, RequestState
from core.models.user import CreatePasswordAuthUserDto
from pydantic import BaseModel

user_router = APIRouter(tags=["User"])


class SignUpRequest(BaseModel):
  username: str
  password: str

@user_router.post("/signup")
def signup(
  data: CreatePasswordAuthUserDto,
  app_state: Annotated[AppState, Depends(get_app_state_dep)],
  request_state: Annotated[RequestState, Depends(get_request_state_dep)],
):
  app_state.repositories.user_repo.insert_password_auth_user(
    request_state.db_session, data
  )
  return APIResponse(message="ok")


