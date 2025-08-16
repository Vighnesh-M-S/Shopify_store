from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import httpx
from app.models import BrandContext, Policy, Contact, Links, FAQ
from app.services import scraper

router = APIRouter()

class StoreRequest(BaseModel):
    website_url: str

@router.post("/fetch_store_insights", response_model=BrandContext)
async def fetch_store_insights(req: StoreRequest):
    try:
        website_url = req.website_url
        if not website_url.startswith("http"):
            website_url = "https://" + website_url

        brand_name = await scraper.get_brand_name(website_url)
        products = await scraper.get_product_catalog(website_url)
        hero_products = await scraper.get_hero_products(website_url)
        policies = await scraper.get_policies(website_url)
        faqs = await scraper.get_faqs(website_url)
        socials = await scraper.get_social_handles(website_url)
        contact = await scraper.get_contact_details(website_url)
        about = await scraper.get_about_text(website_url)
        links = await scraper.get_links(website_url)

        return BrandContext(
            brand_name=brand_name,
            product_catalog=products,
            hero_products=hero_products,
            policies=Policy(**policies) if policies else Policy(),
            faqs=[FAQ(**f) for f in faqs] if faqs else [],
            social_handles=socials,
            contact=Contact(**contact) if contact else Contact(),
            about=about,
            links=Links(**links) if links else Links()
        )
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=401, detail="Website not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

