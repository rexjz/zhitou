from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from enum import Enum


class ReportStatus(str, Enum):
    """报告状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class AnnouncementType(str, Enum):
    """公告类型枚举"""
    Q1_REPORT = "Q1_REPORT"  # XXXX年第一季度报告
    INTERIM_SUMMARY = "INTERIM_SUMMARY"  # XXXX年半年度报告摘要
    INTERIM_REPORT = "INTERIM_REPORT"  # XXXX年半年度报告
    Q3_REPORT = "Q3_REPORT"  # XXXX年第三季度报告
    ANNUAL_SUMMARY = "ANNUAL_SUMMARY"  # XXXX年年度报告摘要
    ANNUAL_REPORT = "ANNUAL_REPORT"  # XXXX年年度报告
    
    @classmethod
    def get_display_name(cls, announcement_type: str, year: int) -> str:
        """获取公告类型的显示名称"""
        type_names = {
            cls.Q1_REPORT: f"{year}年第一季度报告",
            cls.INTERIM_SUMMARY: f"{year}年半年度报告摘要",
            cls.INTERIM_REPORT: f"{year}年半年度报告",
            cls.Q3_REPORT: f"{year}年第三季度报告",
            cls.ANNUAL_SUMMARY: f"{year}年年度报告摘要",
            cls.ANNUAL_REPORT: f"{year}年年度报告",
        }
        return type_names.get(announcement_type, f"{year}年报告")

class AnnouncementFileModel(BaseModel):
    """年报文件领域模型"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    company_id: int
    report_year: int
    report_file_path: Optional[str] = None
    
    # others
    shareholders_equity: Optional[Decimal] = None
    report_status: str
    publish_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm_model(cls, orm_model) -> "AnnouncementFileModel":
        """从 ORM 模型转换"""
        return cls.model_validate(orm_model)


class CreateAnnouncementFileDto(BaseModel):
    """创建年报文件 DTO"""
    company_id: int
    report_year: int
    report_file_path: Optional[str] = None

    shareholders_equity: Optional[Decimal] = None
    report_status: str = ReportStatus.PENDING
    publish_date: Optional[date] = None


class UpdateAnnouncementFileDto(BaseModel):
    """更新年报文件 DTO"""
    report_file_path: Optional[str] = None
    
    shareholders_equity: Optional[Decimal] = None
    report_status: Optional[str] = None
    publish_date: Optional[date] = None