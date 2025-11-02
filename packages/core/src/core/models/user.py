from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from database.orm_models.user import UserOrmModel


class UserModel(BaseModel):
  id: UUID
  username: str
  email: Optional[str]

  @staticmethod
  def from_orm_model(orm_model: UserOrmModel) -> UserModel:
    return UserModel(
      id=orm_model.id, username=orm_model.username, email=orm_model.email
    )

  @staticmethod
  def from_orm_model_list(orm_models: list[UserOrmModel]) -> list[UserModel]:
    return [UserModel.from_orm_model(om) for om in orm_models]


class CreatePasswordAuthUserDto(BaseModel):
  username: str
  email: Optional[str] = None
  hashed_password: str
  salt: str


class UpdateUserDto(BaseModel):
  username: Optional[str] = None
  email: Optional[str] = None
