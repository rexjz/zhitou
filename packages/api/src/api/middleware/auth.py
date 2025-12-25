from typing import Optional
from core.config.models import JWTConfig
from fastapi import Request, HTTPException, status, Depends
from jose import JWTError, jwt
from uuid import UUID
from datetime import datetime, timedelta, timezone
from api.state import get_app_state_dep, RequestState
from core.models.user import UserModel
from loguru import logger


def generate_token(
  jwt_config: JWTConfig,
  user: UserModel,
  expires_delta: Optional[timedelta] = None
) -> str:
  """
  Generate a JWT token for a user.

  Args:
    request: FastAPI request object to access app state
    user: UserModel to generate token for
    expires_delta: Optional expiration time delta (defaults to 7 days)

  Returns:
    JWT token string
  """
  # Set expiration time
  if expires_delta is None:
    expires_delta = timedelta(hours=2)

  now = datetime.now(timezone.utc)
  expire = now + expires_delta

  # Create token payload with Unix epoch timestamps
  payload = {
    "sub": str(user.id),
    "exp": int(expire.timestamp()),
    "iat": int(now.timestamp())
  }

  # Encode token
  token = jwt.encode(
    payload,
    jwt_config.secret_key,
    algorithm=jwt_config.algorithm
  )

  return token


async def get_token_from_cookie(request: Request) -> Optional[str]:
  """
  Extract JWT token from cookie.

  Args:
    request: FastAPI request object

  Returns:
    Token string or None if not found
  """
  app_state = get_app_state_dep(request)
  token = request.cookies.get(app_state.config.jwt.cookie_name)
  return token


async def verify_jwt_token(
  request: Request,
  token: Optional[str] = Depends(get_token_from_cookie)
) -> UserModel:
  """
  Dependency to verify JWT token and return authenticated user.

  Use this as a dependency in route handlers to protect routes.

  Args:
    request: FastAPI request object
    token: JWT token from cookie

  Returns:
    Authenticated UserModel

  Raises:
    HTTPException: If authentication fails

  Example:
    @router.get("/protected")
    def protected_route(user: UserModel = Depends(verify_jwt_token)):
        return {"username": user.username}
  """
  if not token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Authentication token not found"
    )

  app_state = get_app_state_dep(request)
  jwt_config = app_state.config.jwt

  try:
    # Decode JWT token
    payload = jwt.decode(
      token,
      jwt_config.secret_key,
      algorithms=[jwt_config.algorithm]
    )

    # Extract user information from token
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token payload"
      )

    user_id = UUID(user_id_str)

    # Get request state to access db_session
    request_state: RequestState = request.state.r_state

    # Fetch user from database
    user = app_state.repositories.user_repo.find_one_user_by_id(
      request_state.db_session,
      user_id
    )

    return user

  except JWTError as e:
    logger.warning(f"JWT verification failed: {e}")
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or expired token"
    )
  except ValueError as e:
    logger.warning(f"Invalid user ID in token: {e}")
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token payload"
    )
  except Exception as e:
    logger.error(f"Authentication error: {e}")
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Authentication failed"
    )


# Alias for more intuitive usage
get_current_user = verify_jwt_token
