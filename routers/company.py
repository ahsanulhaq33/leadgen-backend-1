from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging
import math

from db.session import get_db_factory
from models.models import Company
from schemas.schemas import CompanyListResponse, CompanyListItem, PaginationParams
from utils.slug_utils import generate_slug
from config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Inject DB session for lead_generation
get_lead_db = get_db_factory("lead_generation")

@router.get("/list", response_model=CompanyListResponse, status_code=status.HTTP_200_OK)
async def get_companies(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(default=None, description="Search company name"),
    db: AsyncSession = Depends(get_lead_db)
):
    """
    Get paginated list of companies with slug generation.
    
    Parameters:
    - page: Page number (default: 1)
    - per_page: Number of items per page (default: 10, max: 100)
    - search: Optional search term for company names
    
    Returns:
    - Paginated list of companies with generated slugs
    """
    try:
        # Validate pagination parameters
        if per_page > settings.max_page_size:
            per_page = settings.max_page_size
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Build base query
        base_query = select(Company)
        count_query = select(func.count(Company.co_rowid))
        
        # Apply search filter if provided
        if search:
            search_term = f"%{search}%"
            base_query = base_query.where(Company.company_name.ilike(search_term))
            count_query = count_query.where(Company.company_name.ilike(search_term))
        
        # Get total count
        total_result = await db.execute(count_query)
        total_count = total_result.scalar() or 0
        
        # Calculate total pages
        total_pages = math.ceil(total_count / per_page) if total_count > 0 else 0
        
        # Validate current page
        if page > total_pages and total_pages > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Page {page} does not exist. Total pages: {total_pages}"
            )
        
        # Get paginated results
        query = base_query.order_by(Company.company_name).offset(offset).limit(per_page)
        result = await db.execute(query)
        companies = result.scalars().all()
        
        # Process companies and generate slugs
        company_list = []
        for company in companies:
            # Generate slug from company name
            slug = generate_slug(company.company_name)
            
            # Create description from available data
            description_parts = []
            if company.market_size:
                description_parts.append(f"Market Size: {company.market_size}")
            if company.company_size:
                description_parts.append(f"Company Size: {company.company_size}")
            if company.revenue_threshold:
                description_parts.append(f"Revenue: {company.revenue_threshold}")
            
            # If no specific data, use pain points or buying triggers as description
            if not description_parts:
                if company.pain_points:
                    description = company.pain_points[:200] + "..." if len(company.pain_points) > 200 else company.pain_points
                elif company.buying_triggers:
                    description = company.buying_triggers[:200] + "..." if len(company.buying_triggers) > 200 else company.buying_triggers
                else:
                    description = "Company profile information available"
            else:
                description = " | ".join(description_parts)
            
            company_item = CompanyListItem(
                company_name=company.company_name,
                company_website=company.company_website,
                company_description=description,
                company_slug=slug
            )
            company_list.append(company_item)
        
        # Prepare response
        response = CompanyListResponse(
            companies_total=total_count,
            companies=company_list,
            total_pages=total_pages,
            current_page=page,
            per_page=per_page
        )
        
        return response
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_companies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while fetching companies"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_companies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.get("/company/{slug}", status_code=status.HTTP_200_OK)
async def get_company_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_lead_db)
):
    """
    Get company details by slug.
    
    Parameters:
    - slug: Company slug (e.g., 'cedar-financial')
    
    Returns:
    - Company details
    """
    try:
        # Get all companies to find matching slug
        result = await db.execute(select(Company))
        companies = result.scalars().all()
        
        # Find company with matching slug
        for company in companies:
            if generate_slug(company.company_name) == slug:
                return {
                    "co_rowid": company.co_rowid,
                    "company_name": company.company_name,
                    "company_website": company.company_website,
                    "linkedin_company_url": company.linkedin_company_url,
                    "is_profiled": company.is_profiled,
                    "market_size": company.market_size,
                    "company_size": company.company_size,
                    "revenue_threshold": company.revenue_threshold,
                    "pain_points": company.pain_points,
                    "buying_triggers": company.buying_triggers,
                    "last_profiled_on": company.last_profiled_on,
                    "company_slug": slug
                }
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with slug '{slug}' not found"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching company by slug: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching company details"
        )