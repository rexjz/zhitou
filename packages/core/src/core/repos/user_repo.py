from core.models.user import UserModel, CreatePasswordAuthUserDto
from .repo import SyncRepository
from database.orm_models.user import UserOrmModel, UserPasswordOrmModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from uuid import UUID
from typing import Protocol, Optional
import hashlib
import secrets


class UserRepository(Protocol):
  def find_one_user_by_id(self, session: Session, id: UUID) -> UserModel:
    ...

  def find_user_by_username(
    self, session: Session, username: str
  ) -> Optional[UserModel]:
    ...

  def insert_password_auth_user(
    self, session: Session, dto: CreatePasswordAuthUserDto
  ) -> UserModel:
    ...


class UserRepositoryImpl:
  _orm_repo = SyncRepository(UserOrmModel, UserModel, UserModel.from_orm_model)

  def find_one_user_by_id(self, session: Session, id: UUID) -> UserModel:
    return self._orm_repo.get(session, id)

  def find_user_by_username(
    self, session: Session, username: str
  ) -> Optional[UserModel]:
    try:
      user_orm = (
        session.query(UserOrmModel)
        .filter(UserOrmModel.username == username)
        .one()
      )
      return UserModel.from_orm_model(user_orm)
    except NoResultFound:
      return None

  def insert_password_auth_user(
    self, session: Session, dto: CreatePasswordAuthUserDto
  ) -> UserModel:
    # Generate salt
    salt = secrets.token_hex(32)

    # Hash password with salt
    password_with_salt = f"{dto.password}{salt}"
    hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()

    savepoint = session.begin_nested()
    try:
      user_orm = UserOrmModel(username=dto.username, email=dto.email)
      session.add(user_orm)
      session.flush()

      password_orm = UserPasswordOrmModel(
        user_id=user_orm.id, hashed_password=hashed_password, salt=salt
      )
      session.add(password_orm)
      session.flush()

      savepoint.commit()
      return UserModel.from_orm_model(user_orm)
    except Exception:
      savepoint.rollback()
      raise
