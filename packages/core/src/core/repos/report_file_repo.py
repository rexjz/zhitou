from typing import Optional, Protocol, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, select, or_, func

from core.models.report_file import (
    AnnouncementFileModel, 
    CreateAnnouncementFileDto, 
    UpdateAnnouncementFileDto,
    ReportStatus,
    AnnouncementType
)
from database.src.database.orm_models.report_file import ChinaCompanyAnnouncementFileOrm
from database.src.database.orm_models.company import ChinaCompanyOrm
from .repo import SyncRepository, PageResult


class AnnouncementFileWithCompany:
    """公告文件关联公司信息的视图模型"""
    def __init__(self, announcement: ChinaCompanyAnnouncementFileOrm):
        self.id = announcement.id
        self.company_id = announcement.company_id
        self.company_code = announcement.company.company_code
        self.full_name = announcement.company.full_name
        self.short_name = announcement.company.short_name
        self.report_year = announcement.report_year
        self.announcement_type = announcement.announcement_type
        self.file_path = announcement.file_path
        self.report_status = announcement.report_status
        self.publish_date = announcement.publish_date
        self.display_name = AnnouncementType.get_display_name(
            announcement.announcement_type, 
            announcement.report_year
        )


class AnnouncementFileRepository(Protocol):
    """公告文件仓储接口"""
    
    def get_by_id(self, session: Session, id: int) -> Optional[AnnouncementFileModel]:
        """根据 ID 查找公告文件"""
        ...
    
    def get_by_company_year_type(
        self, 
        session: Session, 
        company_id: int, 
        report_year: int,
        announcement_type: str
    ) -> Optional[AnnouncementFileModel]:
        """根据企业、年度和类型查找公告文件"""
        ...
    
    def get_by_company_code_year_type(
        self,
        session: Session,
        company_code: str,
        report_year: int,
        announcement_type: str
    ) -> Optional[AnnouncementFileModel]:
        """根据企业代码、年度和类型查找公告文件"""
        ...
    
    def list_by_company(
        self, 
        session: Session, 
        company_id: int,
        announcement_type: Optional[str] = None,
    ) -> list[AnnouncementFileModel]:
        """查询某企业的公告文件列表(按年度降序)"""
        ...
    
    def list_by_company_code(
        self,
        session: Session,
        company_code: str,
        announcement_type: Optional[str] = None,
    ) -> list[AnnouncementFileModel]:
        """根据企业代码查询公告文件列表(按年度降序)"""
        ...
    
    def list_by_year(
        self,
        session: Session,
        report_year: int,
        announcement_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[AnnouncementFileModel]:
        """根据年度查询公告文件列表"""
        ...
    
    def list_by_year_range(
        self,
        session: Session,
        start_year: int,
        end_year: int,
        company_id: Optional[int] = None,
        announcement_type: Optional[str] = None,
    ) -> list[AnnouncementFileModel]:
        """根据年度区间查询公告文件列表"""
        ...
    
    def list_with_company(
        self,
        session: Session,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
        announcement_type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[AnnouncementFileWithCompany]:
        """查询公告文件并关联公司信息"""
        ...
    
    def paginate_with_company(
        self,
        session: Session,
        page: int = 1,
        page_size: int = 20,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
        announcement_type: Optional[str] = None,
    ) -> PageResult[AnnouncementFileWithCompany]:
        """分页查询公告文件并关联公司信息"""
        ...
    
    def get_latest_by_company(
        self, 
        session: Session, 
        company_id: int,
        announcement_type: Optional[str] = None
    ) -> Optional[AnnouncementFileModel]:
        """获取企业最新年度的公告"""
        ...
    
    def create(
        self, 
        session: Session, 
        dto: CreateAnnouncementFileDto
    ) -> AnnouncementFileModel:
        """创建公告文件记录"""
        ...
    
    def create_or_update(
        self,
        session: Session,
        dto: CreateAnnouncementFileDto
    ) -> tuple[AnnouncementFileModel, bool]:
        """创建或更新公告文件记录,返回(模型, 是否为新创建)"""
        ...
    
    def update(
        self, 
        session: Session, 
        id: int, 
        dto: UpdateAnnouncementFileDto
    ) -> Optional[AnnouncementFileModel]:
        """更新公告文件记录"""
        ...
    
    def update_file_path(
        self,
        session: Session,
        id: int,
        file_path: str
    ) -> Optional[AnnouncementFileModel]:
        """更新报告文件路径"""
        ...
    
    def delete(self, session: Session, id: int) -> bool:
        """删除公告文件记录"""
        ...
    
    def exists_by_company_year_type(
        self,
        session: Session,
        company_id: int,
        report_year: int,
        announcement_type: str
    ) -> bool:
        """检查指定企业、年度和类型的公告是否存在"""
        ...


class AnnouncementFileRepositoryImpl:
    """公告文件仓储实现"""
    
    _orm_repo = SyncRepository(
        ChinaCompanyAnnouncementFileOrm,
        AnnouncementFileModel,
        AnnouncementFileModel.from_orm_model
    )
    
    def get_by_id(self, session: Session, id: int) -> Optional[AnnouncementFileModel]:
        """根据 ID 查找公告文件"""
        return self._orm_repo.get(session, id)
    
    def get_by_company_year_type(
        self, 
        session: Session, 
        company_id: int, 
        report_year: int,
        announcement_type: str
    ) -> Optional[AnnouncementFileModel]:
        """根据企业、年度和类型查找公告文件"""
        return self._orm_repo.get_one_by(
            session,
            and_(
                ChinaCompanyAnnouncementFileOrm.company_id == company_id,
                ChinaCompanyAnnouncementFileOrm.report_year == report_year,
                ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type
            )
        )
    
    def get_by_company_code_year_type(
        self,
        session: Session,
        company_code: str,
        report_year: int,
        announcement_type: str
    ) -> Optional[AnnouncementFileModel]:
        """根据企业代码、年度和类型查找公告文件"""
        stmt = (
            select(ChinaCompanyAnnouncementFileOrm)
            .join(ChinaCompanyOrm)
            .where(
                and_(
                    ChinaCompanyOrm.company_code == company_code,
                    ChinaCompanyAnnouncementFileOrm.report_year == report_year,
                    ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type
                )
            )
        )
        result = session.execute(stmt).scalar_one_or_none()
        return AnnouncementFileModel.from_orm_model(result) if result else None
    
    def list_by_company(
        self, 
        session: Session, 
        company_id: int,
        announcement_type: Optional[str] = None,
    ) -> list[AnnouncementFileModel]:
        """查询某企业的公告文件列表(按年度降序)"""
        filters = [ChinaCompanyAnnouncementFileOrm.company_id == company_id]
        if announcement_type:
            filters.append(ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type)
        
        return self._orm_repo.list(
            session,
            *filters,
            order_by=[ChinaCompanyAnnouncementFileOrm.report_year.desc()]
        )
    
    def list_by_company_code(
        self,
        session: Session,
        company_code: str,
        announcement_type: Optional[str] = None,
    ) -> list[AnnouncementFileModel]:
        """根据企业代码查询公告文件列表(按年度降序)"""
        stmt = (
            select(ChinaCompanyAnnouncementFileOrm)
            .join(ChinaCompanyOrm)
            .where(ChinaCompanyOrm.company_code == company_code)
        )
        
        if announcement_type:
            stmt = stmt.where(
                ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type
            )
        
        stmt = stmt.order_by(ChinaCompanyAnnouncementFileOrm.report_year.desc())
        
        results = session.execute(stmt).scalars().all()
        return [AnnouncementFileModel.from_orm_model(r) for r in results]
    
    def list_by_year(
        self,
        session: Session,
        report_year: int,
        announcement_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[AnnouncementFileModel]:
        """根据年度查询公告文件列表"""
        filters = [ChinaCompanyAnnouncementFileOrm.report_year == report_year]
        if announcement_type:
            filters.append(ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type)
        
        return self._orm_repo.list(
            session,
            *filters,
            order_by=[ChinaCompanyAnnouncementFileOrm.created_at.desc()],
            limit=limit
        )
    
    def list_by_year_range(
        self,
        session: Session,
        start_year: int,
        end_year: int,
        company_id: Optional[int] = None,
        announcement_type: Optional[str] = None,
    ) -> list[AnnouncementFileModel]:
        """根据年度区间查询公告文件列表"""
        filters = [
            ChinaCompanyAnnouncementFileOrm.report_year >= start_year,
            ChinaCompanyAnnouncementFileOrm.report_year <= end_year
        ]
        
        if company_id:
            filters.append(ChinaCompanyAnnouncementFileOrm.company_id == company_id)
        if announcement_type:
            filters.append(ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type)
        
        return self._orm_repo.list(
            session,
            *filters,
            order_by=[
                ChinaCompanyAnnouncementFileOrm.report_year.desc(),
                ChinaCompanyAnnouncementFileOrm.company_id
            ]
        )
    
    def list_with_company(
        self,
        session: Session,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
        announcement_type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[AnnouncementFileWithCompany]:
        """查询公告文件并关联公司信息"""
        stmt = (
            select(ChinaCompanyAnnouncementFileOrm)
            .join(ChinaCompanyOrm)
            .options(joinedload(ChinaCompanyAnnouncementFileOrm.company))
        )
        
        if year:
            stmt = stmt.where(ChinaCompanyAnnouncementFileOrm.report_year == year)
        if company_code:
            stmt = stmt.where(ChinaCompanyOrm.company_code == company_code)
        if announcement_type:
            stmt = stmt.where(ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type)

        stmt = stmt.order_by(ChinaCompanyAnnouncementFileOrm.report_year.desc())
        
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        
        results = session.execute(stmt).scalars().all()
        return [AnnouncementFileWithCompany(announcement) for announcement in results]
    
    def paginate_with_company(
        self,
        session: Session,
        page: int = 1,
        page_size: int = 20,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
        announcement_type: Optional[str] = None,
    ) -> PageResult[AnnouncementFileWithCompany]:
        """分页查询公告文件并关联公司信息"""
        # 构建基础查询
        base_stmt = (
            select(ChinaCompanyAnnouncementFileOrm)
            .join(ChinaCompanyOrm)
        )
        
        if year:
            base_stmt = base_stmt.where(ChinaCompanyAnnouncementFileOrm.report_year == year)
        if company_code:
            base_stmt = base_stmt.where(ChinaCompanyOrm.company_code == company_code)
        if announcement_type:
            base_stmt = base_stmt.where(
                ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type
            )

        # 统计总数
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = session.execute(count_stmt).scalar_one()
        
        # 分页查询
        stmt = (
            base_stmt
            .options(joinedload(ChinaCompanyAnnouncementFileOrm.company))
            .order_by(ChinaCompanyAnnouncementFileOrm.report_year.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        
        results = session.execute(stmt).scalars().all()
        items = [AnnouncementFileWithCompany(announcement) for announcement in results]
        
        return PageResult(items=items, total=total, page=page, page_size=page_size)
    
    def get_latest_by_company(
        self, 
        session: Session, 
        company_id: int,
        announcement_type: Optional[str] = None
    ) -> Optional[AnnouncementFileModel]:
        """获取企业最新年度的公告"""
        filters = [ChinaCompanyAnnouncementFileOrm.company_id == company_id]
        if announcement_type:
            filters.append(ChinaCompanyAnnouncementFileOrm.announcement_type == announcement_type)
        
        return self._orm_repo.get_one_by(
            session,
            *filters,
            order_by=[ChinaCompanyAnnouncementFileOrm.report_year.desc()]
        )
    
    def create(
        self, 
        session: Session, 
        dto: CreateAnnouncementFileDto
    ) -> AnnouncementFileModel:
        """创建公告文件记录"""
        # 检查是否已存在同企业同年度同类型的报告
        if self.exists_by_company_year_type(
            session, 
            dto.company_id, 
            dto.report_year,
            dto.announcement_type
        ):
            type_display = AnnouncementType.get_display_name(
                dto.announcement_type, 
                dto.report_year
            )
            raise ValueError(f"企业 {dto.company_id} 的 {type_display} 已存在")

        announcement_orm = ChinaCompanyAnnouncementFileOrm(
            company_id=dto.company_id,
            report_year=dto.report_year,
            announcement_type=dto.announcement_type,
            file_path=dto.file_path,
            shareholders_equity=dto.shareholders_equity,
            report_status=dto.report_status,
            publish_date=dto.publish_date
        )
        session.add(announcement_orm)
        session.flush()
        session.refresh(announcement_orm)
        
        return AnnouncementFileModel.from_orm_model(announcement_orm)
    
    def create_or_update(
        self,
        session: Session,
        dto: CreateAnnouncementFileDto
    ) -> tuple[AnnouncementFileModel, bool]:
        """
        创建或更新公告文件记录
        
        Returns:
            (模型, 是否为新创建)
        """
        existing = self.get_by_company_year_type(
            session, 
            dto.company_id, 
            dto.report_year,
            dto.announcement_type
        )
        
        if existing:
            # 更新已存在的记录
            updated = self.update(
                session,
                existing.id,
                UpdateAnnouncementFileDto(
                    file_path=dto.file_path,
                    shareholders_equity=dto.shareholders_equity,
                    report_status=dto.report_status,
                    publish_date=dto.publish_date
                )
            )
            return updated, False
        else:
            # 创建新记录
            created = self.create(session, dto)
            return created, True
    
    def update(
        self, 
        session: Session, 
        id: int, 
        dto: UpdateAnnouncementFileDto
    ) -> Optional[AnnouncementFileModel]:
        """更新公告文件记录"""
        announcement_orm = session.get(ChinaCompanyAnnouncementFileOrm, id)
        if announcement_orm is None:
            return None
        
        # 只更新提供的字段
        update_data = dto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(announcement_orm, field, value)
        
        session.flush()
        session.refresh(announcement_orm)
        return AnnouncementFileModel.from_orm_model(announcement_orm)
    
    def update_file_path(
        self,
        session: Session,
        id: int,
        file_path: str
    ) -> Optional[AnnouncementFileModel]:
        """更新报告文件路径"""
        return self.update(
            session,
            id,
            UpdateAnnouncementFileDto(file_path=file_path)
        )
    
    def delete(self, session: Session, id: int) -> bool:
        """删除公告文件记录"""
        announcement_orm = session.get(ChinaCompanyAnnouncementFileOrm, id)
        if announcement_orm is None:
            return False
        
        session.delete(announcement_orm)
        session.flush()
        return True
    
    def exists_by_company_year_type(
        self,
        session: Session,
        company_id: int,
        report_year: int,
        announcement_type: str
    ) -> bool:
        """检查指定企业、年度和类型的公告是否存在"""
        return self.get_by_company_year_type(
            session, 
            company_id, 
            report_year,
            announcement_type
        ) is not None