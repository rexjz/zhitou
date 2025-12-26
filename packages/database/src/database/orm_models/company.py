from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .report_file import ChinaReportFileOrm

class ChinaCompanyOrm(Base):
    __tablename__ = "china_company"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    short_name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # 关系
    report_files: Mapped[list["ChinaReportFileOrm"]] = relationship(
        back_populates="company", 
        cascade="all, delete-orphan"
    )