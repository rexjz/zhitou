from typing import Protocol, Optional, List
from sqlalchemy.orm import Session
from core.models.company import CompanyModel, CreateCompanyDto, UpdateCompanyDto
from core.repos.repo import PageResult


class CompanyService(Protocol):
    """企业服务接口"""
    
    def get_company_by_id(self, session: Session, company_id: int) -> Optional[CompanyModel]:
        """
        根据 ID 查询企业
        
        Args:
            session: 数据库会话
            company_id: 企业 ID
            
        Returns:
            企业模型，如果不存在则返回 None
        """
        ...
    
    def get_company_by_code(self, session: Session, company_code: str) -> Optional[CompanyModel]:
        """
        根据股票代码查询企业
        
        Args:
            session: 数据库会话
            company_code: 6位股票代码
            
        Returns:
            企业模型，如果不存在则返回 None
        """
        ...
    
    def list_companies(
        self,
        session: Session,
        page: int = 1,
        page_size: int = 20,
        keyword: Optional[str] = None
    ) -> PageResult[CompanyModel]:
        """
        分页查询企业列表
        
        Args:
            session: 数据库会话
            page: 页码
            page_size: 每页数量
            keyword: 搜索关键词
            
        Returns:
            分页结果
        """
        ...
    
    def create_company(self, session: Session, dto: CreateCompanyDto) -> CompanyModel:
        """
        创建新企业
        
        Args:
            session: 数据库会话
            dto: 创建企业 DTO
            
        Returns:
            创建的企业模型
            
        Raises:
            ValueError: 当企业代码已存在时
        """
        ...
    
    def update_company(
        self,
        session: Session,
        company_id: int,
        dto: UpdateCompanyDto
    ) -> Optional[CompanyModel]:
        """
        更新企业信息
        
        Args:
            session: 数据库会话
            company_id: 企业 ID
            dto: 更新企业 DTO
            
        Returns:
            更新后的企业模型，如果不存在则返回 None
        """
        ...
    
    def delete_company(self, session: Session, company_id: int) -> bool:
        """
        删除企业
        
        Args:
            session: 数据库会话
            company_id: 企业 ID
            
        Returns:
            删除成功返回 True，企业不存在返回 False
        """
        ...
    
    def check_company_exists(self, session: Session, company_code: str) -> bool:
        """
        检查企业代码是否存在
        
        Args:
            session: 数据库会话
            company_code: 企业代码
            
        Returns:
            存在返回 True，否则返回 False
        """
        ...
