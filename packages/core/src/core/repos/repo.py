from dataclasses import dataclass
from typing import Any, Callable, Generic, Optional, Sequence, TypeVar

from pydantic import BaseModel
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import ColumnElement
from database.orm_models.base import Base

ModelT = TypeVar("ModelT", bound=Base)
DomainModelT = TypeVar("DomainModelT", bound=BaseModel)


@dataclass(slots=True)
class PageResult(Generic[ModelT]):
  items: list[ModelT]
  total: int
  page: int
  page_size: int

  @property
  def pages(self) -> int:
    return (self.total + self.page_size - 1) // self.page_size

  @property
  def has_next(self) -> bool:
    return self.page < self.pages

  @property
  def has_prev(self) -> bool:
    return self.page > 1


class _RepoCore(Generic[ModelT, DomainModelT]):
  """Core helpers to build queries for the repository."""

  model: type[ModelT]
  domain_model: type[DomainModelT]
  map_fn: Callable[[ModelT], DomainModelT]

  def __init__(
    self,
    model: type[ModelT],
    domain_model: type[DomainModelT],
    map_fn: Callable[[ModelT], DomainModelT],
  ):
    self.model = model
    self.domain_model = domain_model
    self.map_fn = map_fn

  def _select(self, *filters: ColumnElement[bool] | bool) -> Select[tuple[ModelT]]:
    stmt: Select[tuple[ModelT]] = select(self.model)
    if filters:
      stmt = stmt.filter(*filters)
    return stmt

  def _count_stmt(self, *filters: ColumnElement[bool] | bool) -> Select[tuple[int]]:
    subq = self._select(*filters).subquery()
    return select(func.count()).select_from(subq)

  def _nullable_map(self, orm_model: Optional[ModelT]) -> Optional[DomainModelT]:
    return None if orm_model is None else self.map_fn(orm_model)

  def _map_list(self, orm_models: list[ModelT]) -> list[DomainModelT]:
    return [self.map_fn(om) for om in orm_models]


class SyncRepository(_RepoCore[ModelT, DomainModelT], Generic[ModelT, DomainModelT]):
  def get(self, session: Session, id: Any) -> Optional[ModelT]:
    return self._nullable_map(session.get(self.model, id))

  def get_one_by(
    self, session: Session, *filters: ColumnElement[bool] | bool
  ) -> Optional[DomainModelT]:
    return self._nullable_map(session.execute(self._select(*filters).limit(1)).scalars().first())

  def list(
    self,
    session: Session,
    *filters: ColumnElement[bool] | bool,
    order_by: Optional[Sequence[Any]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
  ) -> list[DomainModelT]:
    stmt = self._select(*filters)
    if order_by:
      stmt = stmt.order_by(*order_by)
    if limit is not None:
      stmt = stmt.limit(limit)
    if offset is not None:
      stmt = stmt.offset(offset)
    return self._map_list(list(session.execute(stmt).scalars().all()))

  def count(self, session: Session, *filters: ColumnElement[bool] | bool) -> int:
    return int(session.execute(self._count_stmt(*filters)).scalar_one())

  def paginate(
    self,
    session: Session,
    page: int = 1,
    page_size: int = 20,
    *filters: ColumnElement[bool] | bool,
    order_by: Optional[Sequence[Any]] = None,
  ) -> PageResult[DomainModelT]:
    assert page >= 1 and page_size >= 1
    total = self.count(session, *filters)
    items = self.list(
      session,
      *filters,
      order_by=order_by,
      limit=page_size,
      offset=(page - 1) * page_size,
    )
    return PageResult(items=items, total=total, page=page, page_size=page_size)
