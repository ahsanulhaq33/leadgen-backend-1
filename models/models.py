from sqlalchemy import Column, String, Text, Date, Boolean, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = "company"
    __table_args__ = {"schema": "dbo"}  # MSSQL schema
    
    co_rowid = Column(BigInteger, primary_key=True, index=True)
    # Map to actual company name field - assuming the table has both ID and name fields
    company_name = Column(String(500), nullable=False, index=True)
    company_website = Column(String(255), nullable=True)
    linkedin_company_url = Column(String(2048), nullable=True)
    is_profiled = Column(Boolean, nullable=True, default=False)
    market_size = Column(Text, nullable=True)  # nvarchar(max) maps to Text
    company_size = Column(Text, nullable=True)  # nvarchar(max) maps to Text
    revenue_threshold = Column(Text, nullable=True)  # nvarchar(max) maps to Text
    pain_points = Column(Text, nullable=True)  # nvarchar(max) maps to Text
    buying_triggers = Column(Text, nullable=True)  # nvarchar(max) maps to Text
    last_profiled_on = Column(Date, nullable=True)  # date type
    
    # Relationship to jobs
    jobs = relationship("JobPost", back_populates="company")

class JobPost(Base):
    __tablename__ = "job_post"
    __table_args__ = {"schema": "dbo"}  # MSSQL schema
    
    jp_rowid = Column(BigInteger, primary_key=True, index=True)
    jp_rowid_company = Column(BigInteger, ForeignKey("dbo.company.co_rowid"), nullable=False, index=True)
    job_title = Column(String(255), nullable=True)
    job_type = Column(String(255), nullable=True)
    job_location = Column(String(255), nullable=True)
    job_url = Column(String(2048), nullable=True)
    posted_at = Column(String(255), nullable=True)
    source = Column(String(255), nullable=True)
    pay = Column(String(255), nullable=True)
    # Note: there is no posted_date column in the DB; using posted_at (string)
    
    # Relationship to company
    company = relationship("Company", back_populates="jobs")