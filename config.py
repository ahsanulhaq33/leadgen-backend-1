from typing import Dict
from pydantic import BaseModel

# Database configurations
DATABASES: Dict[str, Dict[str, str]] = {
    "lead_generation": {
        "type": "mssql+aioodbc",
        "server": "192.168.20.90",
        "username": "AI_lead_gen",
        "password": "Cedar123",
        "database": "lead_generation",
        "driver": "ODBC Driver 17 for SQL Server"
    },
}

# API Configuration
class Settings(BaseModel):
    app_name: str = "Lead Generation API"
    version: str = "1.0.0"
    debug: bool = False
    
    # Pagination defaults
    default_page_size: int = 10
    max_page_size: int = 100

settings = Settings()