from sqlalchemy import String, Integer, ForeignKey, Date, Numeric, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from decimal import Decimal
from .base import Base
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from .company import ChinaCompanyOrm


class AnnouncementType(str, enum.Enum):
    """公告类型枚举"""
    Q1_REPORT = "Q1_REPORT"  # 第一季度报告
    INTERIM_SUMMARY = "INTERIM_SUMMARY"  # 半年度报告摘要
    INTERIM_REPORT = "INTERIM_REPORT"  # 半年度报告
    Q3_REPORT = "Q3_REPORT"  # 第三季度报告
    ANNUAL_SUMMARY = "ANNUAL_SUMMARY"  # 年度报告摘要
    ANNUAL_REPORT = "ANNUAL_REPORT"  # 年度报告


class ChinaCompanyAnnouncementFileOrm(Base):
    __tablename__ = "china_company_announcement_file"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("china_company.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    report_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    announcement_type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        index=True,
        comment="公告类型: Q1_REPORT, INTERIM_SUMMARY, INTERIM_REPORT, Q3_REPORT, ANNUAL_SUMMARY, ANNUAL_REPORT"
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # 财务数据
    shareholders_equity: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=True)
    
    # 状态和日期
    report_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    publish_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    # 关系
    company: Mapped["ChinaCompanyOrm"] = relationship(back_populates="announcement_files")
    
    __table_args__ = (
        # 复合唯一约束: 同一公司同一年度同一类型只能有一份报告
        Index(
            'ix_company_year_type', 
            'company_id', 
            'report_year', 
            'announcement_type', 
            unique=True
        ),
    )