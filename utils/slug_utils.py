import re
from typing import Optional
import unicodedata

def generate_slug(text: Optional[str]) -> str:
    """
    Generate a URL-friendly slug from text.
    
    Args:
        text: Input text to convert to slug
        
    Returns:
        URL-friendly slug string
        
    Examples:
        "Cedar Financial" -> "cedar-financial"
        "Tech@Corp Solutions!" -> "techcorp-solutions"
        "ABC & XYZ Company" -> "abc-xyz-company"
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove accents and convert to ASCII
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Replace common symbols with text equivalents
    replacements = {
        '&': 'and',
        '@': 'at',
        '#': 'number',
        '$': 'dollar',
        '%': 'percent',
        '+': 'plus',
    }
    
    for symbol, replacement in replacements.items():
        text = text.replace(symbol, f' {replacement} ')
    
    # Remove all non-alphanumeric characters except spaces and hyphens
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Replace spaces with hyphens
    text = text.replace(' ', '-')
    
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    return text or 'unnamed'

def generate_unique_slug(base_slug: str, existing_slugs: set) -> str:
    """
    Generate a unique slug by appending a number if necessary.
    
    Args:
        base_slug: The base slug to start with
        existing_slugs: Set of existing slugs to check against
        
    Returns:
        Unique slug string
    """
    if base_slug not in existing_slugs:
        return base_slug
    
    counter = 1
    while f"{base_slug}-{counter}" in existing_slugs:
        counter += 1
    
    return f"{base_slug}-{counter}"