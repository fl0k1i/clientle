from pydantic import BaseModel
from typing import Optional


class PriceFilter(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class SearchFilters(BaseModel):
    brand_ids: Optional[list[str]] = None
    gender: Optional[str] = None
    condition: Optional[str] = None
    price: Optional[PriceFilter] = None
    website_ids: Optional[list[str]] = None
    category_ids: Optional[list[str]] = None
    exclude_brand_ids: Optional[list[str]] = None
    exclude_website_ids: Optional[list[str]] = None
    availability: Optional[list[str]] = None


class SearchConfig(BaseModel):
    language: Optional[str] = None
    country: Optional[str] = None
    currency: Optional[str] = None
    keyword_search_only: bool = False


class SearchRequest(BaseModel):
    query: Optional[str] = None
    image_url: Optional[str] = None
    base64_image: Optional[str] = None
    limit: Optional[int] = 20
    page_token: Optional[str] = None
    filters: SearchFilters = SearchFilters()
    config: SearchConfig = SearchConfig()
    