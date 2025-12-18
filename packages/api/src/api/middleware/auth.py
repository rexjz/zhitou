from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from uuid import UUID
from api.state import AppState
from core.models.user import UserModel
from loguru import logger
from typing import cast


class JWTAuthMiddleware:
  """JWT + Cookie authentication middleware."""

  def __init__(self, exclude_paths: Optional[list[str]] = None):
    """
    Initialize the JWT auth middleware.

    Args:
      exclude_paths: List of paths to exclude from authentication (e.g., ["/health", "/login"])
    """
    self.exclude_paths = exclude_paths or ["/health", "/"]

  async def __call__(self, request: Request, call_next):
    """
    Middleware to verify JWT token from cookie.

    Adds user information to request.state if authentication succeeds.
    """
    # Skip authentication for excluded paths
    if request.url.path in self.exclude_paths or self._is_path_excluded(request.url.path):
      return await call_next(request)

    app_state = cast(AppState, request.app.state.state)
    jwt_config = app_state.config.jwt

    # Get token from cookie
    token = request.cookies.get(jwt_config.cookie_name)

    if not token:
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Not authenticated", "message": "Authentication token not found"}
      )

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

      # Fetch user from database
      user = app_state.repositories.user_repo.find_one_user_by_id(
        request.state.r_state.db_session,
        user_id
      )

      # Add user to request state
      request.state.user = user

    except JWTError as e:
      logger.warning(f"JWT verification failed: {e}")
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid or expired token", "message": str(e)}
      )
    except ValueError as e:
      logger.warning(f"Invalid user ID in token: {e}")
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid token payload", "message": "Invalid user ID"}
      )
    except Exception as e:
      logger.error(f"Authentication error: {e}")
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Authentication failed", "message": str(e)}
      )

    # Continue to next middleware/route
    response = await call_next(request)
    return response

  def _is_path_excluded(self, path: str) -> bool:
    """Check if path should be excluded from authentication."""
    for excluded_path in self.exclude_paths:
      if path.startswith(excluded_path):
        return True
    return False


def get_current_user(request: Request) -> UserModel:
  """
  Dependency to get the current authenticated user from request state.

  Raises:
    HTTPException: If user is not authenticated
  """
  user = getattr(request.state, "user", None)
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Not authenticated"
    )
  return user
