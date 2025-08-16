from fastapi import APIRouter, HTTPException
from app.models import BrandContext, Policy, Contact, Links
from app.services import scraper

router = APIRouter()

@router.post("/fetch_store_insights", response_model=BrandContext)
async def fetch_store_insights(website_url: str):
    try:
        # ensure http scheme
        if not website_url.startswith("http"):
            website_url = "https://" + website_url

        # scrape data
        brand_name = await scraper.get_brand_name(website_url)
        products = await scraper.get_product_catalog(website_url)
        hero_products = await scraper.get_hero_products(website_url)

        # build response object (others left empty for now)
        return BrandContext(
            brand_name=brand_name,
            product_catalog=products,
            hero_products=hero_products,
            policies=Policy(),
            faqs=[],
            social_handles={},
            contact=Contact(),
            about=None,
            links=Links()
        )
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=401, detail="Website not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))