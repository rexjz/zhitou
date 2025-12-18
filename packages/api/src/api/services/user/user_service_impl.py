import hashlib
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from core.models.user import UserModel
from core.repos.user_repo import UserRepository
from database.orm_models.user import UserPasswordOrmModel


class UserServiceImpl:
  def __init__(self, user_repo: UserRepository):
    self._user_repo = user_repo

  def verify_user_password(
    self, session: Session, username: str, password: str
  ) -> Optional[UserModel]:
    """
    Verify user identity by checking password with salt hash.
    Returns the UserModel if authentication succeeds, None otherwise.
    """
    try:
      # Find user by username using repository
      user = self._user_repo.find_user_by_username(session, username)
      if not user:
        return None

      # Get the password record for this user
      password_orm = (
        session.query(UserPasswordOrmModel)
        .filter(UserPasswordOrmModel.user_id == user.id)
        .one()
      )

      # Hash the provided password with the stored salt
      hashed_input = self._hash_password(password, password_orm.salt)

      # Compare with stored hash
      if hashed_input == password_orm.hashed_password:
        return user
      else:
        return None

    except NoResultFound:
      return None

  @staticmethod
  def _hash_password(password: str, salt: str) -> str:
    """
    Hash a password with the given salt using SHA-256.
    Returns the hexadecimal digest of the hash.
    """
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode()).hexdigest()
