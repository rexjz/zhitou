from typing import Optional, Protocol, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, select, or_

from core.models.report_file import (
    ReportFileModel, 
    CreateReportFileDto, 
    UpdateReportFileDto,
    ReportStatus
)
from database.orm_models.report_file import ChinaReportFileOrm
from database.orm_models.company import ChinaCompanyOrm
from .repo import SyncRepository, PageResult


class ReportFileWithCompany:
    """年报文件关联公司信息的视图模型"""
    def __init__(self, report: ChinaReportFileOrm):
        self.id = report.id
        self.company_id = report.company_id
        self.company_code = report.company.company_code
        self.full_name = report.company.full_name
        self.short_name = report.company.short_name
        self.report_year = report.report_year
        self.report_file_path = report.report_file_path
        self.report_status = report.report_status

class ReportFileRepository(Protocol):
    """年报文件仓储接口"""
    
    def get_by_id(self, session: Session, id: int) -> Optional[ReportFileModel]:
        """根据 ID 查找年报文件"""
        ...
    
    def get_by_company_and_year(
        self, 
        session: Session, 
        company_id: int, 
        report_year: int
    ) -> Optional[ReportFileModel]:
        """根据企业和年度查找年报文件"""
        ...
    
    def get_by_company_code_and_year(
        self,
        session: Session,
        company_code: str,
        report_year: int
    ) -> Optional[ReportFileModel]:
        """根据企业代码和年度查找年报文件"""
        ...
    
    def list_by_company(
        self, 
        session: Session, 
        company_id: int,
    ) -> list[ReportFileModel]:
        """查询某企业的年报文件列表(按年度降序)"""
        ...
    
    def list_by_company_code(
        self,
        session: Session,
        company_code: str,
    ) -> list[ReportFileModel]:
        """根据企业代码查询年报文件列表(按年度降序)"""
        ...
    
    def list_by_year(
        self,
        session: Session,
        report_year: int,
        limit: Optional[int] = None,
    ) -> list[ReportFileModel]:
        """根据年度查询年报文件列表"""
        ...
    
    def list_by_year_range(
        self,
        session: Session,
        start_year: int,
        end_year: int,
        company_id: Optional[int] = None,
    ) -> list[ReportFileModel]:
        """根据年度区间查询年报文件列表"""
        ...
    
    def list_with_company(
        self,
        session: Session,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[ReportFileWithCompany]:
        """查询年报文件并关联公司信息"""
        ...
    
    def paginate_with_company(
        self,
        session: Session,
        page: int = 1,
        page_size: int = 20,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
    ) -> PageResult[ReportFileWithCompany]:
        """分页查询年报文件并关联公司信息"""
        ...
    
    def get_latest_by_company(
        self, 
        session: Session, 
        company_id: int
    ) -> Optional[ReportFileModel]:
        """获取企业最新年度的年报"""
        ...
    
    def create(
        self, 
        session: Session, 
        dto: CreateReportFileDto
    ) -> ReportFileModel:
        """创建年报文件记录"""
        ...
    
    def create_or_update(
        self,
        session: Session,
        dto: CreateReportFileDto
    ) -> tuple[ReportFileModel, bool]:
        """创建或更新年报文件记录,返回(模型, 是否为新创建)"""
        ...
    
    def update(
        self, 
        session: Session, 
        id: int, 
        dto: UpdateReportFileDto
    ) -> Optional[ReportFileModel]:
        """更新年报文件记录"""
        ...
    
    def update_file_path(
        self,
        session: Session,
        id: int,
        file_path: str
    ) -> Optional[ReportFileModel]:
        """更新报告文件路径"""
        ...
    
    def delete(self, session: Session, id: int) -> bool:
        """删除年报文件记录"""
        ...
    
    def exists_by_company_and_year(
        self,
        session: Session,
        company_id: int,
        report_year: int
    ) -> bool:
        """检查指定企业和年度的年报是否存在"""
        ...


class ReportFileRepositoryImpl:
    """年报文件仓储实现"""
    
    _orm_repo = SyncRepository(
        ChinaReportFileOrm,
        ReportFileModel,
        ReportFileModel.from_orm_model
    )
    
    def get_by_id(self, session: Session, id: int) -> Optional[ReportFileModel]:
        """根据 ID 查找年报文件"""
        return self._orm_repo.get(session, id)
    
    def get_by_company_and_year(
        self, 
        session: Session, 
        company_id: int, 
        report_year: int
    ) -> Optional[ReportFileModel]:
        """根据企业和年度查找年报文件"""
        return self._orm_repo.get_one_by(
            session,
            and_(
                ChinaReportFileOrm.company_id == company_id,
                ChinaReportFileOrm.report_year == report_year
            )
        )
    
    def get_by_company_code_and_year(
        self,
        session: Session,
        company_code: str,
        report_year: int
    ) -> Optional[ReportFileModel]:
        """根据企业代码和年度查找年报文件"""
        stmt = (
            select(ChinaReportFileOrm)
            .join(ChinaCompanyOrm)
            .where(
                and_(
                    ChinaCompanyOrm.company_code == company_code,
                    ChinaReportFileOrm.report_year == report_year
                )
            )
        )
        result = session.execute(stmt).scalar_one_or_none()
        return ReportFileModel.from_orm_model(result) if result else None
    
    def list_by_company(
        self, 
        session: Session, 
        company_id: int,
    ) -> list[ReportFileModel]:
        """查询某企业的年报文件列表(按年度降序)"""
        return self._orm_repo.list(
            session,
            ChinaReportFileOrm.company_id == company_id,
            order_by=[ChinaReportFileOrm.report_year.desc()]
        )
    
    def list_by_company_code(
        self,
        session: Session,
        company_code: str,
    ) -> list[ReportFileModel]:
        """根据企业代码查询年报文件列表(按年度降序)"""
        stmt = (
            select(ChinaReportFileOrm)
            .join(ChinaCompanyOrm)
            .where(ChinaCompanyOrm.company_code == company_code)
            .order_by(ChinaReportFileOrm.report_year.desc())
        )
        results = session.execute(stmt).scalars().all()
        return [ReportFileModel.from_orm_model(r) for r in results]
    
    def list_by_year(
        self,
        session: Session,
        report_year: int,
        limit: Optional[int] = None,
    ) -> list[ReportFileModel]:
        """根据年度查询年报文件列表"""
        return self._orm_repo.list(
            session,
            ChinaReportFileOrm.report_year == report_year,
            order_by=[ChinaReportFileOrm.created_at.desc()],
            limit=limit
        )
    
    def list_by_year_range(
        self,
        session: Session,
        start_year: int,
        end_year: int,
        company_id: Optional[int] = None,
    ) -> list[ReportFileModel]:
        """根据年度区间查询年报文件列表"""
        filters = [
            ChinaReportFileOrm.report_year >= start_year,
            ChinaReportFileOrm.report_year <= end_year
        ]
        
        if company_id:
            filters.append(ChinaReportFileOrm.company_id == company_id)
        
        return self._orm_repo.list(
            session,
            *filters,
            order_by=[
                ChinaReportFileOrm.report_year.desc(),
                ChinaReportFileOrm.company_id
            ]
        )
    
    def list_with_company(
        self,
        session: Session,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[ReportFileWithCompany]:
        """查询年报文件并关联公司信息"""
        stmt = (
            select(ChinaReportFileOrm)
            .join(ChinaCompanyOrm)
            .options(joinedload(ChinaReportFileOrm.company))
        )
        
        if year:
            stmt = stmt.where(ChinaReportFileOrm.report_year == year)
        if company_code:
            stmt = stmt.where(ChinaCompanyOrm.company_code == company_code)

        stmt = stmt.order_by(ChinaReportFileOrm.report_year.desc())
        
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        
        results = session.execute(stmt).scalars().all()
        return [ReportFileWithCompany(report) for report in results]
    
    def paginate_with_company(
        self,
        session: Session,
        page: int = 1,
        page_size: int = 20,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
    ) -> PageResult[ReportFileWithCompany]:
        """分页查询年报文件并关联公司信息"""
        # 构建基础查询
        base_stmt = (
            select(ChinaReportFileOrm)
            .join(ChinaCompanyOrm)
        )
        
        if year:
            base_stmt = base_stmt.where(ChinaReportFileOrm.report_year == year)
        if company_code:
            base_stmt = base_stmt.where(ChinaCompanyOrm.company_code == company_code)

        # 统计总数
        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = session.execute(count_stmt).scalar_one()
        
        # 分页查询
        stmt = (
            base_stmt
            .options(joinedload(ChinaReportFileOrm.company))
            .order_by(ChinaReportFileOrm.report_year.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        
        results = session.execute(stmt).scalars().all()
        items = [ReportFileWithCompany(report) for report in results]
        
        return PageResult(items=items, total=total, page=page, page_size=page_size)
    
    def get_latest_by_company(
        self, 
        session: Session, 
        company_id: int
    ) -> Optional[ReportFileModel]:
        """获取企业最新年度的年报"""
        return self._orm_repo.get_one_by(
            session,
            ChinaReportFileOrm.company_id == company_id,
            order_by=[ChinaReportFileOrm.report_year.desc()]
        )
    
    def create(
        self, 
        session: Session, 
        dto: CreateReportFileDto
    ) -> ReportFileModel:
        """创建年报文件记录"""
        # 检查是否已存在同企业同年度的报告
        if self.exists_by_company_and_year(session, dto.company_id, dto.report_year):
            raise ValueError(
                f"企业 {dto.company_id} 的 {dto.report_year} 年度报告已存在"
            )

        report_orm = ChinaReportFileOrm(
            company_id=dto.company_id,
            report_year=dto.report_year,
            report_file_path=dto.report_file_path,
            shareholders_equity=dto.shareholders_equity,
            report_status=dto.report_status,
            publish_date=dto.publish_date
        )
        session.add(report_orm)
        session.flush()
        session.refresh(report_orm)
        
        return ReportFileModel.from_orm_model(report_orm)
    
    def create_or_update(
        self,
        session: Session,
        dto: CreateReportFileDto
    ) -> tuple[ReportFileModel, bool]:
        """
        创建或更新年报文件记录
        
        Returns:
            (模型, 是否为新创建)
        """
        existing = self.get_by_company_and_year(
            session, 
            dto.company_id, 
            dto.report_year
        )
        
        if existing:
            # 更新已存在的记录
            updated = self.update(
                session,
                existing.id,
                UpdateReportFileDto(
                    report_file_path=dto.report_file_path,
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
        dto: UpdateReportFileDto
    ) -> Optional[ReportFileModel]:
        """更新年报文件记录"""
        report_orm = session.get(ChinaReportFileOrm, id)
        if report_orm is None:
            return None
        
        # 只更新提供的字段
        update_data = dto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(report_orm, field, value)
        
        session.flush()
        session.refresh(report_orm)
        return ReportFileModel.from_orm_model(report_orm)
    
    def update_file_path(
        self,
        session: Session,
        id: int,
        file_path: str
    ) -> Optional[ReportFileModel]:
        """更新报告文件路径"""
        return self.update(
            session,
            id,
            UpdateReportFileDto(report_file_path=file_path)
        )
    
    def delete(self, session: Session, id: int) -> bool:
        """删除年报文件记录"""
        report_orm = session.get(ChinaReportFileOrm, id)
        if report_orm is None:
            return False
        
        session.delete(report_orm)
        session.flush()
        return True
    
    def exists_by_company_and_year(
        self,
        session: Session,
        company_id: int,
        report_year: int
    ) -> bool:
        """检查指定企业和年度的年报是否存在"""
        return self.get_by_company_and_year(session, company_id, report_year) is not None