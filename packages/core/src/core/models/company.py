from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class CompanyModel(BaseModel):
    """china_company 领域模型"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    company_code: str
    full_name: str
    short_name: str


    @classmethod
    def from_orm_model(cls, orm_model) -> "CompanyModel":
        """从 ORM 模型转换"""
        return cls.model_validate(orm_model)
    
class CreateCompanyDto(BaseModel):
    """创建企业 DTO"""
    company_code: str = Field(..., min_length=6, max_length=6, description="6位股票代码")
    full_name: str = Field(..., min_length=1, max_length=200, description="企业全称")
    short_name: Optional[str] = Field(None, max_length=100, description="企业简称")


class UpdateCompanyDto(BaseModel):
    """更新企业 DTO"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    short_name: Optional[str] = Field(None, max_length=100)


class CompanyQueryDto(BaseModel):
    """企业查询 DTO"""
    keyword: Optional[str] = Field(None, description="搜索关键词(代码/全称/简称)")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")