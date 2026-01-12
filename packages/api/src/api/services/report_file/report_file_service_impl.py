from typing import Optional, List
from sqlalchemy.orm import Session
from loguru import logger

from core.models.report_file import AnnouncementFileModel, CreateAnnouncementFileDto, UpdateAnnouncementFileDto
from core.repos.report_file_repo import AnnouncementFileRepository, AnnouncementFileWithCompany
from core.repos.repo import PageResult


class ReportFileServiceImpl:
    """公告文件服务实现"""
    
    def __init__(self, report_file_repo: AnnouncementFileRepository):
        self._report_file_repo = report_file_repo
    
    def get_announcement_by_id(
        self,
        session: Session,
        announcement_id: int
    ) -> Optional[AnnouncementFileModel]:
        """根据 ID 查询公告文件"""
        logger.debug(f"Getting announcement by id: {announcement_id}")
        return self._report_file_repo.get_by_id(session, announcement_id)
    
    def get_announcement_by_company_year_type(
        self,
        session: Session,
        company_id: int,
        report_year: int,
        announcement_type: str
    ) -> Optional[AnnouncementFileModel]:
        """根据企业、年度和类型查询公告文件"""
        logger.debug(
            f"Getting announcement: company_id={company_id}, "
            f"year={report_year}, type={announcement_type}"
        )
        return self._report_file_repo.get_by_company_year_type(
            session, company_id, report_year, announcement_type
        )
    
    def list_announcements_by_company(
        self,
        session: Session,
        company_id: int,
        announcement_type: Optional[str] = None
    ) -> List[AnnouncementFileModel]:
        """查询某企业的公告文件列表"""
        logger.debug(f"Listing announcements for company: {company_id}, type={announcement_type}")
        return self._report_file_repo.list_by_company(
            session, company_id, announcement_type
        )
    
    def list_announcements_by_company_code(
        self,
        session: Session,
        company_code: str,
        announcement_type: Optional[str] = None
    ) -> List[AnnouncementFileModel]:
        """根据企业代码查询公告文件列表"""
        logger.debug(f"Listing announcements for company code: {company_code}, type={announcement_type}")
        return self._report_file_repo.list_by_company_code(
            session, company_code, announcement_type
        )
    
    def list_announcements_by_year(
        self,
        session: Session,
        report_year: int,
        announcement_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[AnnouncementFileModel]:
        """根据年度查询公告文件列表"""
        logger.debug(f"Listing announcements for year: {report_year}, type={announcement_type}, limit={limit}")
        return self._report_file_repo.list_by_year(
            session, report_year, announcement_type, limit
        )
    
    def list_announcements_with_company(
        self,
        session: Session,
        page: int = 1,
        page_size: int = 20,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
        announcement_type: Optional[str] = None
    ) -> PageResult[AnnouncementFileWithCompany]:
        """分页查询公告文件并关联公司信息"""
        logger.debug(
            f"Listing announcements with company: page={page}, page_size={page_size}, "
            f"year={year}, company_code={company_code}, type={announcement_type}"
        )
        return self._report_file_repo.paginate_with_company(
            session=session,
            page=page,
            page_size=page_size,
            year=year,
            company_code=company_code,
            announcement_type=announcement_type
        )
    
    def create_announcement(
        self,
        session: Session,
        dto: CreateAnnouncementFileDto
    ) -> AnnouncementFileModel:
        """
        创建公告文件
        
        Raises:
            ValueError: 当同企业同年度同类型的公告已存在时
        """
        logger.info(
            f"Creating announcement: company_id={dto.company_id}, "
            f"year={dto.report_year}, type={dto.announcement_type}"
        )
        
        # 业务逻辑：检查是否已存在
        if self._report_file_repo.exists_by_company_year_type(
            session, dto.company_id, dto.report_year, dto.announcement_type
        ):
            raise ValueError(
                f"企业 {dto.company_id} 的 {dto.report_year} 年 "
                f"{dto.announcement_type} 类型公告已存在"
            )
        
        return self._report_file_repo.create(session, dto)
    
    def update_announcement(
        self,
        session: Session,
        announcement_id: int,
        dto: UpdateAnnouncementFileDto
    ) -> Optional[AnnouncementFileModel]:
        """更新公告文件信息"""
        logger.info(f"Updating announcement: {announcement_id}")
        
        # 业务逻辑：检查公告是否存在
        existing = self._report_file_repo.get_by_id(session, announcement_id)
        if existing is None:
            logger.warning(f"Announcement not found: {announcement_id}")
            return None
        
        return self._report_file_repo.update(session, announcement_id, dto)
    
    def delete_announcement(self, session: Session, announcement_id: int) -> bool:
        """
        删除公告文件
        
        Returns:
            删除成功返回 True，公告不存在返回 False
        """
        logger.info(f"Deleting announcement: {announcement_id}")
        
        # 业务逻辑：检查公告是否存在
        existing = self._report_file_repo.get_by_id(session, announcement_id)
        if existing is None:
            logger.warning(f"Announcement not found: {announcement_id}")
            return False
        
        return self._report_file_repo.delete(session, announcement_id)
    
    def check_announcement_exists(
        self,
        session: Session,
        company_id: int,
        report_year: int,
        announcement_type: str
    ) -> bool:
        """检查指定企业、年度和类型的公告是否存在"""
        return self._report_file_repo.exists_by_company_year_type(
            session, company_id, report_year, announcement_type
        )
