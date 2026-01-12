from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, Optional, List
from pydantic import BaseModel, Field

from api.middleware import get_current_user
from api.api_models.api_response import APIResponse
from api.state import get_app_state_dep, get_request_state_dep, AppState, RequestState
from core.models.report_file import (
    AnnouncementFileModel, 
    CreateAnnouncementFileDto, 
    UpdateAnnouncementFileDto,
    AnnouncementType
)
from core.repos.repo import PageResult
from loguru import logger

report_file_router = APIRouter(dependencies=[Depends(get_current_user)], tags=["ReportFile"])


class AnnouncementFileResponseData(BaseModel):
    """Announcement file response model"""
    id: int = Field(..., description="Announcement file ID")
    company_id: int = Field(..., description="Company ID")
    report_year: int = Field(..., description="Report year")
    announcement_type: str = Field(..., description="Announcement type")
    file_path: Optional[str] = Field(None, description="File path")


class AnnouncementFileWithCompanyData(BaseModel):
    """Announcement file with company info"""
    id: int
    company_id: int
    company_code: str
    full_name: str
    short_name: Optional[str]
    report_year: int
    announcement_type: str
    file_path: Optional[str]
    display_name: str


class AnnouncementFileListResponseData(BaseModel):
    """Announcement file list response model"""
    items: List[AnnouncementFileResponseData] = Field(..., description="Announcement file list")
    total: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")


class AnnouncementFileWithCompanyListResponseData(BaseModel):
    """Announcement file with company list response model"""
    items: List[AnnouncementFileWithCompanyData] = Field(..., description="Announcement file list with company info")
    total: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")


class CreateAnnouncementFileRequest(BaseModel):
    """Create announcement file request"""
    company_id: int = Field(..., description="Company ID")
    report_year: int = Field(..., description="Report year")
    announcement_type: str = Field(..., description="Announcement type")
    file_path: Optional[str] = Field(None, description="File path")


class UpdateAnnouncementFileRequest(BaseModel):
    """Update announcement file request"""
    file_path: Optional[str] = Field(None, description="File path")


@report_file_router.post("", operation_id="create_announcement_file")
def create_announcement_file(
    data: CreateAnnouncementFileRequest,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[AnnouncementFileResponseData]:
    """
    Create a new announcement file
    
    Args:
        data: Announcement file creation data
        
    Returns:
        Created announcement file information
        
    Raises:
        HTTPException: If announcement already exists for this company, year, and type
    """
    try:
        dto = CreateAnnouncementFileDto(
            company_id=data.company_id,
            report_year=data.report_year,
            announcement_type=data.announcement_type,
            file_path=data.file_path
        )
        
        announcement = app_state.services.report_file_service.create_announcement(
            request_state.db_session, dto
        )
        request_state.db_session.commit()
        
        return APIResponse[AnnouncementFileResponseData](
            message="Announcement file created successfully",
            data=AnnouncementFileResponseData(
                id=announcement.id,
                company_id=announcement.company_id,
                report_year=announcement.report_year,
                announcement_type=announcement.announcement_type,
                file_path=announcement.file_path
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@report_file_router.get("/{announcement_id}", operation_id="get_announcement_file_by_id")
def get_announcement_file_by_id(
    announcement_id: int,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[AnnouncementFileResponseData]:
    """
    Get announcement file by ID
    
    Args:
        announcement_id: Announcement file ID
        
    Returns:
        Announcement file information
        
    Raises:
        HTTPException: If announcement file not found
    """
    announcement = app_state.services.report_file_service.get_announcement_by_id(
        request_state.db_session, announcement_id
    )
    
    if announcement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Announcement file with ID {announcement_id} not found"
        )
    
    return APIResponse[AnnouncementFileResponseData](
        message="",
        data=AnnouncementFileResponseData(
            id=announcement.id,
            company_id=announcement.company_id,
            report_year=announcement.report_year,
            announcement_type=announcement.announcement_type,
            file_path=announcement.file_path
        )
    )


@report_file_router.get("/company/{company_id}", operation_id="list_announcement_files_by_company")
def list_announcement_files_by_company(
    company_id: int,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
    announcement_type: Optional[str] = Query(None, description="Filter by announcement type"),
) -> APIResponse[List[AnnouncementFileResponseData]]:
    """
    List announcement files by company ID
    
    Args:
        company_id: Company ID
        announcement_type: Optional filter by announcement type
        
    Returns:
        List of announcement files (sorted by year desc)
    """
    announcements = app_state.services.report_file_service.list_announcements_by_company(
        request_state.db_session,
        company_id=company_id,
        announcement_type=announcement_type
    )
    
    return APIResponse[List[AnnouncementFileResponseData]](
        message="",
        data=[
            AnnouncementFileResponseData(
                id=announcement.id,
                company_id=announcement.company_id,
                report_year=announcement.report_year,
                announcement_type=announcement.announcement_type,
                file_path=announcement.file_path
            ) for announcement in announcements
        ]
    )


@report_file_router.get("/company/code/{company_code}", operation_id="list_announcement_files_by_company_code")
def list_announcement_files_by_company_code(
    company_code: str,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
    announcement_type: Optional[str] = Query(None, description="Filter by announcement type"),
) -> APIResponse[List[AnnouncementFileResponseData]]:
    """
    List announcement files by company code
    
    Args:
        company_code: Company stock code
        announcement_type: Optional filter by announcement type
        
    Returns:
        List of announcement files (sorted by year desc)
    """
    announcements = app_state.services.report_file_service.list_announcements_by_company_code(
        request_state.db_session,
        company_code=company_code,
        announcement_type=announcement_type
    )
    
    return APIResponse[List[AnnouncementFileResponseData]](
        message="",
        data=[
            AnnouncementFileResponseData(
                id=announcement.id,
                company_id=announcement.company_id,
                report_year=announcement.report_year,
                announcement_type=announcement.announcement_type,
                file_path=announcement.file_path
            ) for announcement in announcements
        ]
    )


@report_file_router.get("", operation_id="list_announcement_files_with_company")
def list_announcement_files_with_company(
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    year: Optional[int] = Query(None, description="Filter by report year"),
    company_code: Optional[str] = Query(None, description="Filter by company code"),
    announcement_type: Optional[str] = Query(None, description="Filter by announcement type"),
) -> APIResponse[AnnouncementFileWithCompanyListResponseData]:
    """
    List announcement files with company information (paginated)
    
    Args:
        page: Page number (starts from 1)
        page_size: Number of items per page
        year: Filter by report year
        company_code: Filter by company code
        announcement_type: Filter by announcement type
        
    Returns:
        Paginated announcement file list with company info
    """
    result = app_state.services.report_file_service.list_announcements_with_company(
        request_state.db_session,
        page=page,
        page_size=page_size,
        year=year,
        company_code=company_code,
        announcement_type=announcement_type
    )
    
    return APIResponse[AnnouncementFileWithCompanyListResponseData](
        message="",
        data=AnnouncementFileWithCompanyListResponseData(
            items=[
                AnnouncementFileWithCompanyData(
                    id=item.id,
                    company_id=item.company_id,
                    company_code=item.company_code,
                    full_name=item.full_name,
                    short_name=item.short_name,
                    report_year=item.report_year,
                    announcement_type=item.announcement_type,
                    file_path=item.file_path,
                    display_name=item.display_name
                ) for item in result.items
            ],
            total=result.total,
            page=result.page,
            page_size=result.page_size
        )
    )


@report_file_router.put("/{announcement_id}", operation_id="update_announcement_file")
def update_announcement_file(
    announcement_id: int,
    data: UpdateAnnouncementFileRequest,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[AnnouncementFileResponseData]:
    """
    Update announcement file information
    
    Args:
        announcement_id: Announcement file ID
        data: Announcement file update data
        
    Returns:
        Updated announcement file information
        
    Raises:
        HTTPException: If announcement file not found
    """
    dto = UpdateAnnouncementFileDto(
        file_path=data.file_path
    )
    
    announcement = app_state.services.report_file_service.update_announcement(
        request_state.db_session, announcement_id, dto
    )
    
    if announcement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Announcement file with ID {announcement_id} not found"
        )
    
    request_state.db_session.commit()
    
    return APIResponse[AnnouncementFileResponseData](
        message="Announcement file updated successfully",
        data=AnnouncementFileResponseData(
            id=announcement.id,
            company_id=announcement.company_id,
            report_year=announcement.report_year,
            announcement_type=announcement.announcement_type,
            file_path=announcement.file_path
        )
    )


@report_file_router.delete("/{announcement_id}", operation_id="delete_announcement_file")
def delete_announcement_file(
    announcement_id: int,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[None]:
    """
    Delete announcement file
    
    Args:
        announcement_id: Announcement file ID
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If announcement file not found
    """
    success = app_state.services.report_file_service.delete_announcement(
        request_state.db_session, announcement_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Announcement file with ID {announcement_id} not found"
        )
    
    request_state.db_session.commit()
    
    return APIResponse[None](message="Announcement file deleted successfully")


@report_file_router.get("/year/{report_year}", operation_id="list_announcement_files_by_year")
def list_announcement_files_by_year(
    report_year: int,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
    announcement_type: Optional[str] = Query(None, description="Filter by announcement type"),
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Limit results"),
) -> APIResponse[List[AnnouncementFileResponseData]]:
    """
    List announcement files by report year
    
    Args:
        report_year: Report year
        announcement_type: Optional filter by announcement type
        limit: Optional limit on number of results
        
    Returns:
        List of announcement files
    """
    announcements = app_state.services.report_file_service.list_announcements_by_year(
        request_state.db_session,
        report_year=report_year,
        announcement_type=announcement_type,
        limit=limit
    )
    
    return APIResponse[List[AnnouncementFileResponseData]](
        message="",
        data=[
            AnnouncementFileResponseData(
                id=announcement.id,
                company_id=announcement.company_id,
                report_year=announcement.report_year,
                announcement_type=announcement.announcement_type,
                file_path=announcement.file_path
            ) for announcement in announcements
        ]
    )
