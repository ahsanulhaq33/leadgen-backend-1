from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class CompanyBase(BaseModel):
    company_name: str
    company_website: Optional[str] = None
    linkedin_company_url: Optional[str] = None
    is_profiled: Optional[bool] = False
    market_size: Optional[str] = None
    company_size: Optional[str] = None
    revenue_threshold: Optional[str] = None
    pain_points: Optional[str] = None
    buying_triggers: Optional[str] = None
    last_profiled_on: Optional[datetime] = None

class CompanyListItem(BaseModel):
    """Schema for company list response"""
    company_name: str
    company_website: Optional[str] = None
    company_description: Optional[str] = None
    company_slug: str
    
    class Config:
        from_attributes = True

class CompanyListResponse(BaseModel):
    """Paginated company list response"""
    companies_total: int = Field(description="Total number of companies")
    companies: List[CompanyListItem] = Field(description="List of companies")
    total_pages: int = Field(description="Total number of pages")
    current_page: int = Field(description="Current page number")
    per_page: int = Field(description="Items per page")
    
    @validator('companies_total', 'total_pages', 'current_page', 'per_page', pre=True)
    def convert_to_int(cls, v):
        """Ensure integer fields are properly typed"""
        return int(v) if v is not None else 0

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=10, ge=1, le=100, description="Items per page")
    search: Optional[str] = Field(default=None, description="Search term for company name")
    
    @validator('per_page')
    def validate_per_page(cls, v):
        if v > 100:
            return 100
        if v < 1:
            return 10
        return v

# Job-related schemas
class JobItem(BaseModel):
    """Schema for individual job item"""
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    job_location: Optional[str] = None
    job_type: Optional[str] = None
    job_url: Optional[str] = None
    job_posted_date: Optional[str] = None
    job_pay_rate: Optional[str] = None
    job_source: Optional[str] = None
    
    class Config:
        from_attributes = True

class CompanyJobsResponse(BaseModel):
    """Response schema for company jobs with pagination"""
    total_position: int = Field(description="Total number of job positions")
    jobs: List[JobItem] = Field(description="List of jobs")
    total_pages: int = Field(description="Total number of pages")
    page_size: int = Field(description="Items per page")
    current_page: int = Field(description="Current page number")
    
    @validator('total_position', 'total_pages', 'current_page', 'page_size', pre=True)
    def convert_to_int(cls, v):
        """Ensure integer fields are properly typed"""
        return int(v) if v is not None else 0