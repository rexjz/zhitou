from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base

class UserOrm(Base):
  __tablename__ = "user"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  username = Column(String(50), unique=True, nullable=False)
  email = Column(String(100), unique=True, nullable=True)

  password = relationship("UserPasswordOrm", back_populates="user", uselist=False)

  def __repr__(self):
    return f"<UserOrm(id={self.id}, username='{self.username}', email='{self.email}')>"


class UserPasswordOrm(Base):
  __tablename__ = "user_password"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), unique=True, nullable=False)
  hashed_password = Column(String(255), nullable=False)

  user = relationship("UserOrm", back_populates="password")

  def __repr__(self):
    return f"<UserPasswordOrm(user_id={self.user_id})>"
