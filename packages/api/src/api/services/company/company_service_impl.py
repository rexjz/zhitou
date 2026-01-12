from typing import Optional
from sqlalchemy.orm import Session
from loguru import logger

from core.models.company import CompanyModel, CreateCompanyDto, UpdateCompanyDto
from core.repos.company_repo import CompanyRepository
from core.repos.repo import PageResult


class CompanyServiceImpl:
    """企业服务实现"""
    
    def __init__(self, company_repo: CompanyRepository):
        self._company_repo = company_repo
    
    def get_company_by_id(self, session: Session, company_id: int) -> Optional[CompanyModel]:
        """根据 ID 查询企业"""
        logger.debug(f"Getting company by id: {company_id}")
        return self._company_repo.get_by_id(session, company_id)
    
    def get_company_by_code(self, session: Session, company_code: str) -> Optional[CompanyModel]:
        """根据股票代码查询企业"""
        logger.debug(f"Getting company by code: {company_code}")
        return self._company_repo.get_by_code(session, company_code)
    
    def list_companies(
        self,
        session: Session,
        page: int = 1,
        page_size: int = 20,
        keyword: Optional[str] = None
    ) -> PageResult[CompanyModel]:
        """分页查询企业列表"""
        logger.debug(f"Listing companies: page={page}, page_size={page_size}, keyword={keyword}")
        return self._company_repo.paginate(
            session,
            page=page,
            page_size=page_size,
            keyword=keyword
        )
    
    def create_company(self, session: Session, dto: CreateCompanyDto) -> CompanyModel:
        """
        创建新企业
        
        Raises:
            ValueError: 当企业代码已存在时
        """
        logger.info(f"Creating company: {dto.company_code}")
        
        # 业务逻辑：检查企业代码是否已存在
        if self._company_repo.exists_by_code(session, dto.company_code):
            raise ValueError(f"企业代码 {dto.company_code} 已存在")
        
        return self._company_repo.create(session, dto)
    
    def update_company(
        self,
        session: Session,
        company_id: int,
        dto: UpdateCompanyDto
    ) -> Optional[CompanyModel]:
        """更新企业信息"""
        logger.info(f"Updating company: {company_id}")
        
        # 业务逻辑：检查企业是否存在
        existing = self._company_repo.get_by_id(session, company_id)
        if existing is None:
            logger.warning(f"Company not found: {company_id}")
            return None
        
        return self._company_repo.update(session, company_id, dto)
    
    def delete_company(self, session: Session, company_id: int) -> bool:
        """
        删除企业（级联删除关联的公告文件）
        
        Returns:
            删除成功返回 True，企业不存在返回 False
        """
        logger.info(f"Deleting company: {company_id}")
        
        # 业务逻辑：检查企业是否存在
        existing = self._company_repo.get_by_id(session, company_id)
        if existing is None:
            logger.warning(f"Company not found: {company_id}")
            return False
        
        return self._company_repo.delete(session, company_id)
    
    def check_company_exists(self, session: Session, company_code: str) -> bool:
        """检查企业代码是否存在"""
        return self._company_repo.exists_by_code(session, company_code)
