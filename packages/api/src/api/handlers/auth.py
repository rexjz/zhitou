from api.middleware.auth import generate_token
from fastapi import APIRouter, Response, HTTPException, status
from typing import Annotated
from api.api_models.api_response import APIResponse
from fastapi import Depends
from api.state import get_app_state_dep, get_request_state_dep, AppState, RequestState
from core.models.user import CreatePasswordAuthUserDto
from pydantic import BaseModel

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/signup")
def signup(
  data: CreatePasswordAuthUserDto,
  app_state: Annotated[AppState, Depends(get_app_state_dep)],
  request_state: Annotated[RequestState, Depends(get_request_state_dep)],
):
  app_state.repositories.user_repo.insert_password_auth_user(
    request_state.db_session, data
  )
  return APIResponse(message="ok")


class SignInRequest(BaseModel):
  username: str
  password: str


@auth_router.post("/signin/upass")
def signin(
  data: SignInRequest,
  response: Response,
  app_state: Annotated[AppState, Depends(get_app_state_dep)],
  request_state: Annotated[RequestState, Depends(get_request_state_dep)],
):
  user = app_state.services.user_service.verify_user_password(
    request_state.db_session, data.username, data.password
  )

  if user is not None:
    token = generate_token(jwt_config=app_state.config.jwt, user=user)

    response.set_cookie(
      key=app_state.config.jwt.cookie_name,
      value=token,
      httponly=True,
      secure=app_state.config.jwt.cookie_secure,
      samesite="lax",
      max_age=7200,
    )

    return APIResponse(message="Sign in successful")
  else:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
