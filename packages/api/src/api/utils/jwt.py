from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from uuid import UUID
from core.config.models import JWTConfig


def create_access_token(
  user_id: UUID,
  jwt_config: JWTConfig,
  expires_delta: Optional[timedelta] = None
) -> str:
  """
  Create a JWT access token for a user.

  Args:
    user_id: The user's UUID
    jwt_config: JWT configuration
    expires_delta: Optional custom expiration time

  Returns:
    Encoded JWT token string
  """
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(
      minutes=jwt_config.access_token_expire_minutes
    )

  to_encode = {
    "sub": str(user_id),
    "exp": expire,
    "iat": datetime.utcnow()
  }

  encoded_jwt = jwt.encode(
    to_encode,
    jwt_config.secret_key,
    algorithm=jwt_config.algorithm
  )

  return encoded_jwt


def decode_token(token: str, jwt_config: JWTConfig) -> dict:
  """
  Decode and verify a JWT token.

  Args:
    token: The JWT token string
    jwt_config: JWT configuration

  Returns:
    Decoded token payload

  Raises:
    JWTError: If token is invalid or expired
  """
  payload = jwt.decode(
    token,
    jwt_config.secret_key,
    algorithms=[jwt_config.algorithm]
  )
  return payload
