from typing import Protocol, Optional
from sqlalchemy.orm import Session
from core.models.user import UserModel


class UserService(Protocol):
  def verify_user_password(
    self, session: Session, username: str, password: str
  ) -> Optional[UserModel]:
    """
    Verify user identity by checking password with salt hash.
    Returns the UserModel if authentication succeeds, None otherwise.
    """
    ...
