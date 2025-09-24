from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = "company"
    __table_args__ = {"schema": "dbo"}  # MSSQL schema
    
    co_rowid = Column(BigInteger, primary_key=True, index=True)
    company_name = Column(String(500), nullable=False, index=True)
    company_website = Column(String(500), nullable=True)
    linkedin_company_url = Column(String(500), nullable=True)
    is_profiled = Column(Boolean, nullable=True, default=False)
    market_size = Column(String(100), nullable=True)
    company_size = Column(String(100), nullable=True)
    revenue_threshold = Column(String(100), nullable=True)
    pain_points = Column(Text, nullable=True)
    buying_triggers = Column(Text, nullable=True)
    last_profiled_on = Column(DateTime, nullable=True)