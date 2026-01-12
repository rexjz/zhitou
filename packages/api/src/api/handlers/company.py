from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, Optional, List
from pydantic import BaseModel, Field

from api.middleware import get_current_user
from api.api_models.api_response import APIResponse
from api.state import get_app_state_dep, get_request_state_dep, AppState, RequestState
from core.models.company import CompanyModel, CreateCompanyDto, UpdateCompanyDto
from core.repos.repo import PageResult
from loguru import logger

company_router = APIRouter(dependencies=[Depends(get_current_user)], tags=["Company"])


class CompanyResponseData(BaseModel):
    """Company response model"""
    id: int = Field(..., description="Company ID")
    company_code: str = Field(..., description="6-digit stock code")
    full_name: str = Field(..., description="Full company name")
    short_name: Optional[str] = Field(None, description="Short company name")


class CompanyListResponseData(BaseModel):
    """Company list response model"""
    items: List[CompanyResponseData] = Field(..., description="Company list")
    total: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")


class CreateCompanyRequest(BaseModel):
    """Create company request"""
    company_code: str = Field(..., min_length=6, max_length=6, description="6-digit stock code")
    full_name: str = Field(..., min_length=1, max_length=200, description="Full company name")
    short_name: Optional[str] = Field(None, max_length=100, description="Short company name")


class UpdateCompanyRequest(BaseModel):
    """Update company request"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=200, description="Full company name")
    short_name: Optional[str] = Field(None, max_length=100, description="Short company name")


@company_router.post("", operation_id="create_company")
def create_company(
    data: CreateCompanyRequest,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[CompanyResponseData]:
    """
    Create a new company
    
    Args:
        data: Company creation data
        
    Returns:
        Created company information
        
    Raises:
        HTTPException: If company code already exists
    """
    try:
        dto = CreateCompanyDto(
            company_code=data.company_code,
            full_name=data.full_name,
            short_name=data.short_name
        )
        
        company = app_state.services.company_service.create_company(
            request_state.db_session, dto
        )
        request_state.db_session.commit()
        
        return APIResponse[CompanyResponseData](
            message="Company created successfully",
            data=CompanyResponseData(
                id=company.id,
                company_code=company.company_code,
                full_name=company.full_name,
                short_name=company.short_name
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@company_router.get("/{company_id}", operation_id="get_company_by_id")
def get_company_by_id(
    company_id: int,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[CompanyResponseData]:
    """
    Get company by ID
    
    Args:
        company_id: Company ID
        
    Returns:
        Company information
        
    Raises:
        HTTPException: If company not found
    """
    company = app_state.services.company_service.get_company_by_id(
        request_state.db_session, company_id
    )
    
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found"
        )
    
    return APIResponse[CompanyResponseData](
        message="",
        data=CompanyResponseData(
            id=company.id,
            company_code=company.company_code,
            full_name=company.full_name,
            short_name=company.short_name
        )
    )


@company_router.get("/code/{company_code}", operation_id="get_company_by_code")
def get_company_by_code(
    company_code: str,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[CompanyResponseData]:
    """
    Get company by stock code
    
    Args:
        company_code: 6-digit stock code
        
    Returns:
        Company information
        
    Raises:
        HTTPException: If company not found
    """
    company = app_state.services.company_service.get_company_by_code(
        request_state.db_session, company_code
    )
    
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with code {company_code} not found"
        )
    
    return APIResponse[CompanyResponseData](
        message="",
        data=CompanyResponseData(
            id=company.id,
            company_code=company.company_code,
            full_name=company.full_name,
            short_name=company.short_name
        )
    )


@company_router.get("", operation_id="list_companies")
def list_companies(
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    keyword: Optional[str] = Query(None, description="Search keyword (code/full name/short name)"),
) -> APIResponse[CompanyListResponseData]:
    """
    List companies with pagination
    
    Args:
        page: Page number (starts from 1)
        page_size: Number of items per page
        keyword: Search keyword for fuzzy search by code, full name, or short name
        
    Returns:
        Paginated company list
    """
    result = app_state.services.company_service.list_companies(
        request_state.db_session,
        page=page,
        page_size=page_size,
        keyword=keyword
    )
    
    return APIResponse[CompanyListResponseData](
        message="",
        data=CompanyListResponseData(
            items=[
                CompanyResponseData(
                    id=company.id,
                    company_code=company.company_code,
                    full_name=company.full_name,
                    short_name=company.short_name
                ) for company in result.items
            ],
            total=result.total,
            page=result.page,
            page_size=result.page_size
        )
    )


@company_router.put("/{company_id}", operation_id="update_company")
def update_company(
    company_id: int,
    data: UpdateCompanyRequest,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[CompanyResponseData]:
    """
    Update company information
    
    Args:
        company_id: Company ID
        data: Company update data
        
    Returns:
        Updated company information
        
    Raises:
        HTTPException: If company not found
    """
    dto = UpdateCompanyDto(
        full_name=data.full_name,
        short_name=data.short_name
    )
    
    company = app_state.services.company_service.update_company(
        request_state.db_session, company_id, dto
    )
    
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found"
        )
    
    request_state.db_session.commit()
    
    return APIResponse[CompanyResponseData](
        message="Company updated successfully",
        data=CompanyResponseData(
            id=company.id,
            company_code=company.company_code,
            full_name=company.full_name,
            short_name=company.short_name
        )
    )


@company_router.delete("/{company_id}", operation_id="delete_company")
def delete_company(
    company_id: int,
    app_state: Annotated[AppState, Depends(get_app_state_dep)],
    request_state: Annotated[RequestState, Depends(get_request_state_dep)],
) -> APIResponse[None]:
    """
    Delete company (cascade delete related announcement files)
    
    Args:
        company_id: Company ID
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If company not found
    """
    success = app_state.services.company_service.delete_company(
        request_state.db_session, company_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found"
        )
    
    request_state.db_session.commit()
    
    return APIResponse[None](message="Company deleted successfully")
