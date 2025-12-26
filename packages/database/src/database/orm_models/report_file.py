from sqlalchemy import String, Integer, ForeignKey, Date, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from decimal import Decimal
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .company import ChinaCompanyOrm

class ChinaReportFileOrm(Base):
    __tablename__ = "china_report_file"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("china_company.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    report_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    report_file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # others
    shareholders_equity: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=True)
    report_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    publish_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    # 关系
    company: Mapped["ChinaCompanyOrm"] = relationship(back_populates="report_files")
    
    __table_args__ = (
        # 复合唯一约束:同一公司同一年度只能有一份报告
        Index('ix_company_year', 'company_id', 'report_year', unique=True),
    )
