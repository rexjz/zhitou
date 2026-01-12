from typing import Protocol, Optional, List
from sqlalchemy.orm import Session
from core.models.report_file import AnnouncementFileModel, CreateAnnouncementFileDto, UpdateAnnouncementFileDto
from core.repos.report_file_repo import AnnouncementFileWithCompany
from core.repos.repo import PageResult


class ReportFileService(Protocol):
    """公告文件服务接口"""
    
    def get_announcement_by_id(
        self,
        session: Session,
        announcement_id: int
    ) -> Optional[AnnouncementFileModel]:
        """
        根据 ID 查询公告文件
        
        Args:
            session: 数据库会话
            announcement_id: 公告文件 ID
            
        Returns:
            公告文件模型，如果不存在则返回 None
        """
        ...
    
    def get_announcement_by_company_year_type(
        self,
        session: Session,
        company_id: int,
        report_year: int,
        announcement_type: str
    ) -> Optional[AnnouncementFileModel]:
        """
        根据企业、年度和类型查询公告文件
        
        Args:
            session: 数据库会话
            company_id: 企业 ID
            report_year: 报告年度
            announcement_type: 公告类型
            
        Returns:
            公告文件模型，如果不存在则返回 None
        """
        ...
    
    def list_announcements_by_company(
        self,
        session: Session,
        company_id: int,
        announcement_type: Optional[str] = None
    ) -> List[AnnouncementFileModel]:
        """
        查询某企业的公告文件列表
        
        Args:
            session: 数据库会话
            company_id: 企业 ID
            announcement_type: 可选的公告类型过滤
            
        Returns:
            公告文件列表（按年度降序）
        """
        ...
    
    def list_announcements_by_company_code(
        self,
        session: Session,
        company_code: str,
        announcement_type: Optional[str] = None
    ) -> List[AnnouncementFileModel]:
        """
        根据企业代码查询公告文件列表
        
        Args:
            session: 数据库会话
            company_code: 企业代码
            announcement_type: 可选的公告类型过滤
            
        Returns:
            公告文件列表（按年度降序）
        """
        ...
    
    def list_announcements_by_year(
        self,
        session: Session,
        report_year: int,
        announcement_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[AnnouncementFileModel]:
        """
        根据年度查询公告文件列表
        
        Args:
            session: 数据库会话
            report_year: 报告年度
            announcement_type: 可选的公告类型过滤
            limit: 限制返回数量
            
        Returns:
            公告文件列表
        """
        ...
    
    def list_announcements_with_company(
        self,
        session: Session,
        page: int = 1,
        page_size: int = 20,
        year: Optional[int] = None,
        company_code: Optional[str] = None,
        announcement_type: Optional[str] = None
    ) -> PageResult[AnnouncementFileWithCompany]:
        """
        分页查询公告文件并关联公司信息
        
        Args:
            session: 数据库会话
            page: 页码
            page_size: 每页数量
            year: 年度过滤
            company_code: 企业代码过滤
            announcement_type: 公告类型过滤
            
        Returns:
            分页结果
        """
        ...
    
    def create_announcement(
        self,
        session: Session,
        dto: CreateAnnouncementFileDto
    ) -> AnnouncementFileModel:
        """
        创建公告文件
        
        Args:
            session: 数据库会话
            dto: 创建公告文件 DTO
            
        Returns:
            创建的公告文件模型
            
        Raises:
            ValueError: 当同企业同年度同类型的公告已存在时
        """
        ...
    
    def update_announcement(
        self,
        session: Session,
        announcement_id: int,
        dto: UpdateAnnouncementFileDto
    ) -> Optional[AnnouncementFileModel]:
        """
        更新公告文件信息
        
        Args:
            session: 数据库会话
            announcement_id: 公告文件 ID
            dto: 更新公告文件 DTO
            
        Returns:
            更新后的公告文件模型，如果不存在则返回 None
        """
        ...
    
    def delete_announcement(self, session: Session, announcement_id: int) -> bool:
        """
        删除公告文件
        
        Args:
            session: 数据库会话
            announcement_id: 公告文件 ID
            
        Returns:
            删除成功返回 True，公告不存在返回 False
        """
        ...
    
    def check_announcement_exists(
        self,
        session: Session,
        company_id: int,
        report_year: int,
        announcement_type: str
    ) -> bool:
        """
        检查指定企业、年度和类型的公告是否存在
        
        Args:
            session: 数据库会话
            company_id: 企业 ID
            report_year: 报告年度
            announcement_type: 公告类型
            
        Returns:
            存在返回 True，否则返回 False
        """
        ...
