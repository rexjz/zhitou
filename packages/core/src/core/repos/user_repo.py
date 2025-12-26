from core.models.user import UserModel, CreatePasswordAuthUserDto
from .repo import SyncRepository
from database.orm_models.user import UserOrmModel, UserPasswordOrmModel
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Protocol


class UserRepository(Protocol):
  def find_one_user_by_id(self, session: Session, id: UUID) -> UserModel:
    ...

  def insert_password_auth_user(
    self, session: Session, dto: CreatePasswordAuthUserDto
  ) -> UserModel:
    ...


class UserRepositoryImpl:
  _orm_repo = SyncRepository(UserOrmModel, UserModel, UserModel.from_orm_model)

  def find_one_user_by_id(self, session: Session, id: UUID) -> UserModel:
    return self._orm_repo.get(session, id)

  def insert_password_auth_user(
    self, session: Session, dto: CreatePasswordAuthUserDto
  ) -> UserModel:
    savepoint = session.begin_nested()
    try:
      user_orm = UserOrmModel(username=dto.username, email=dto.email)
      session.add(user_orm)
      session.flush()

      password_orm = UserPasswordOrmModel(
        user_id=user_orm.id, hashed_password=dto.hashed_password, salt=dto.salt
      )
      session.add(password_orm)
      session.flush()

      savepoint.commit()
      return UserModel.from_orm_model(user_orm)
    except Exception:
      savepoint.rollback()
      raise
