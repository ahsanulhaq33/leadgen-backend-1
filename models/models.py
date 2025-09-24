from sqlalchemy import Column, String, Text, Date, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base

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