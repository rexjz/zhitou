from typing import Optional, Protocol
from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.models.company import CompanyModel, CreateCompanyDto, UpdateCompanyDto
from database.orm_models.company import ChinaCompanyOrm
from .repo import SyncRepository, PageResult


class CompanyRepository(Protocol):
    """企业仓储接口"""
    
    def get_by_id(self, session: Session, id: int) -> Optional[CompanyModel]:
        """根据 ID 查找企业"""
        ...
    
    def get_by_code(self, session: Session, company_code: str) -> Optional[CompanyModel]:
        """根据企业代码查找企业"""
        ...
    
    def get_by_full_name(self, session: Session, full_name: str) -> Optional[CompanyModel]:
        """根据企业全称查找企业"""
        ...
    
    def get_by_short_name(self, session: Session, short_name: str) -> Optional[CompanyModel]:
        """根据企业简称查找企业"""
        ...
    
    def list_all(
        self, 
        session: Session,
        keyword: Optional[str] = None,
        order_by: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[CompanyModel]:
        """查询企业列表"""
        ...
    
    def paginate(
        self, 
        session: Session, 
        page: int = 1, 
        page_size: int = 20,
        keyword: Optional[str] = None,
    ) -> PageResult[CompanyModel]:
        """分页查询企业列表"""
        ...
    
    def create(self, session: Session, dto: CreateCompanyDto) -> CompanyModel:
        """创建新企业"""
        ...
    
    def update(self, session: Session, id: int, dto: UpdateCompanyDto) -> Optional[CompanyModel]:
        """更新企业信息"""
        ...
    
    def delete(self, session: Session, id: int) -> bool:
        """删除企业"""
        ...
    
    def exists_by_code(self, session: Session, company_code: str) -> bool:
        """检查企业代码是否存在"""
        ...


class CompanyRepositoryImpl:
    """企业仓储实现"""
    
    _orm_repo = SyncRepository(
        ChinaCompanyOrm, 
        CompanyModel, 
        CompanyModel.from_orm_model
    )
    
    def get_by_id(self, session: Session, id: int) -> Optional[CompanyModel]:
        """根据 ID 查找企业"""
        return self._orm_repo.get(session, id)
    
    def get_by_code(self, session: Session, company_code: str) -> Optional[CompanyModel]:
        """根据企业代码查找企业"""
        return self._orm_repo.get_one_by(
            session,
            ChinaCompanyOrm.company_code == company_code
        )
    
    def get_by_full_name(self, session: Session, full_name: str) -> Optional[CompanyModel]:
        """根据企业全称精确查找企业"""
        return self._orm_repo.get_one_by(
            session,
            ChinaCompanyOrm.full_name == full_name
        )
    
    def get_by_short_name(self, session: Session, short_name: str) -> Optional[CompanyModel]:
        """根据企业简称精确查找企业"""
        return self._orm_repo.get_one_by(
            session,
            ChinaCompanyOrm.short_name == short_name
        )
    
    def list_all(
        self, 
        session: Session,
        keyword: Optional[str] = None,
        order_by: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[CompanyModel]:
        """
        查询企业列表
        
        Args:
            session: 数据库会话
            keyword: 搜索关键词，支持按代码、全称、简称模糊搜索
            order_by: 排序字段列表
            limit: 限制返回数量
            offset: 偏移量
        """
        filters = []
        if keyword:
            # 支持按代码、全称或简称模糊搜索
            filters.append(
                or_(
                    ChinaCompanyOrm.company_code.contains(keyword),
                    ChinaCompanyOrm.full_name.contains(keyword),
                    ChinaCompanyOrm.short_name.contains(keyword)
                )
            )
        
        return self._orm_repo.list(
            session,
            *filters,
            order_by=order_by or [ChinaCompanyOrm.created_at.desc()],
            limit=limit,
            offset=offset
        )
    
    def paginate(
        self, 
        session: Session, 
        page: int = 1, 
        page_size: int = 20,
        keyword: Optional[str] = None,
    ) -> PageResult[CompanyModel]:
        """
        分页查询企业列表
        
        Args:
            session: 数据库会话
            page: 页码(从1开始)
            page_size: 每页数量
            keyword: 搜索关键词，支持按代码、全称、简称模糊搜索
        """
        filters = []
        if keyword:
            filters.append(
                or_(
                    ChinaCompanyOrm.company_code.contains(keyword),
                    ChinaCompanyOrm.full_name.contains(keyword),
                    ChinaCompanyOrm.short_name.contains(keyword)
                )
            )
        
        return self._orm_repo.paginate(
            session,
            page=page,
            page_size=page_size,
            *filters,
            order_by=[ChinaCompanyOrm.created_at.desc()]
        )
    
    def create(self, session: Session, dto: CreateCompanyDto) -> CompanyModel:
        """
        创建新企业
        
        Args:
            session: 数据库会话
            dto: 创建企业DTO
            
        Returns:
            创建的企业模型
            
        Raises:
            ValueError: 当企业代码已存在时
        """
        # 检查企业代码是否已存在
        if self.exists_by_code(session, dto.company_code):
            raise ValueError(f"企业代码 {dto.company_code} 已存在")
        
        company_orm = ChinaCompanyOrm(
            company_code=dto.company_code,
            full_name=dto.full_name,
            short_name=dto.short_name
        )
        session.add(company_orm)
        session.flush()
        session.refresh(company_orm)
        
        return CompanyModel.from_orm_model(company_orm)
    
    def update(self, session: Session, id: int, dto: UpdateCompanyDto) -> Optional[CompanyModel]:
        """
        更新企业信息
        
        Args:
            session: 数据库会话
            id: 企业ID
            dto: 更新企业DTO
            
        Returns:
            更新后的企业模型，如果企业不存在则返回None
        """
        company_orm = session.get(ChinaCompanyOrm, id)
        if company_orm is None:
            return None
        
        # 只更新提供的字段
        update_data = dto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(company_orm, field, value)
        
        session.flush()
        session.refresh(company_orm)
        return CompanyModel.from_orm_model(company_orm)
    
    def delete(self, session: Session, id: int) -> bool:
        """
        删除企业(级联删除关联的年报文件)
        
        Args:
            session: 数据库会话
            id: 企业ID
            
        Returns:
            删除成功返回True，企业不存在返回False
        """
        company_orm = session.get(ChinaCompanyOrm, id)
        if company_orm is None:
            return False
        
        session.delete(company_orm)
        session.flush()
        return True
    
    def exists_by_code(self, session: Session, company_code: str) -> bool:
        """
        检查企业代码是否存在
        
        Args:
            session: 数据库会话
            company_code: 企业代码
            
        Returns:
            存在返回True，否则返回False
        """
        return self.get_by_code(session, company_code) is not None