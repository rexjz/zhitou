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


class ReportFileModel(BaseModel):
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
    def from_orm_model(cls, orm_model) -> "ReportFileModel":
        """从 ORM 模型转换"""
        return cls.model_validate(orm_model)


class CreateReportFileDto(BaseModel):
    """创建年报文件 DTO"""
    company_id: int
    report_year: int
    report_file_path: Optional[str] = None

    shareholders_equity: Optional[Decimal] = None
    report_status: str = ReportStatus.PENDING
    publish_date: Optional[date] = None


class UpdateReportFileDto(BaseModel):
    """更新年报文件 DTO"""
    report_file_path: Optional[str] = None
    
    shareholders_equity: Optional[Decimal] = None
    report_status: Optional[str] = None
    publish_date: Optional[date] = None