from typing import List, Dict, Optional
from pydantic import BaseModel

class Policy(BaseModel):
    privacy_policy: Optional[str] = None
    return_policy: Optional[str] = None

class FAQ(BaseModel):
    question: str
    answer: str

class Contact(BaseModel):
    emails: List[str] = []
    phones: List[str] = []

class Links(BaseModel):
    order_tracking: Optional[str] = None
    contact_us: Optional[str] = None
    blogs: Optional[str] = None

class BrandContext(BaseModel):
    brand_name: Optional[str] = None
    product_catalog: List[Dict] = []
    hero_products: List[Dict] = []
    policies: Policy
    faqs: List[FAQ] = []
    social_handles: Dict[str, str] = {}
    contact: Contact
    about: Optional[str] = None
    links: Links