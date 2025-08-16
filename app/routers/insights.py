from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import httpx
from app.models import BrandContext, Policy, Contact, Links, FAQ, CompetitorRequest
from app.services import scraper
from app.services.competitor_finder import find_competitors
from app.db import SessionLocal
from app import models_db
from sqlalchemy.orm import joinedload

router = APIRouter()

class StoreRequest(BaseModel):
    website_url: str

@router.post("/get_competitors")
async def get_competitors(req: CompetitorRequest):
    main_url = req.website_url
    competitors = req.competitor_urls or await find_competitors(main_url)
    return {"main": main_url, "competitors": competitors}

def get_brand_context_from_db(url: str) -> BrandContext | None:
    db = SessionLocal()
    try:
        brand = (
            db.query(models_db.Brand)
            .options(
                joinedload(models_db.Brand.products),
                joinedload(models_db.Brand.policies),
                joinedload(models_db.Brand.contact),
            )
            .filter(models_db.Brand.url == url)
            .first()
        )
        if not brand:
            return None

        return BrandContext(
            brand_name=brand.name,
            about=brand.about,
            product_catalog=[{"title": p.title, "price": p.price, "url": p.url} for p in brand.products],
            hero_products=[],
            policies=Policy(
                privacy_policy=brand.policies.privacy_policy if brand.policies else None,
                return_policy=brand.policies.return_policy if brand.policies else None,
            ),
            faqs=[],
            social_handles={},
            contact=Contact(
                emails=brand.contact.emails if brand.contact else [],
                phones=brand.contact.phones if brand.contact else [],
                address=brand.contact.address if brand.contact else None,
            ),
            links=Links()
        )
    finally:
        db.close()
async def save_to_db(insights: BrandContext, url: str):
    db = SessionLocal()
    try:
        brand = models_db.Brand(
            name=insights.brand_name,
            url=url,
            about=insights.about,
        )
        db.add(brand)
        db.flush()  # so brand.id is available

        # Products
        for p in insights.product_catalog:
            db.add(models_db.Product(
                title=p.get("title"),
                price=p.get("price"),
                url=p.get("handle") if "handle" in p else None,
                brand_id=brand.id
            ))

        # ✅ Policies (use attributes, not .get)
        if insights.policies:
            db.add(models_db.PolicyDB(
                privacy_policy=insights.policies.privacy_policy,
                return_policy=insights.policies.return_policy,
                brand_id=brand.id
            ))

        # ✅ Contact
        if insights.contact:
            db.add(models_db.ContactDB(
                emails=insights.contact.emails if hasattr(insights.contact, "emails") else [],
                phones=insights.contact.phones if hasattr(insights.contact, "phones") else [],
                address=getattr(insights.contact, "address", None),
                brand_id=brand.id
            ))

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@router.post("/fetch_store_insights", response_model=BrandContext)
async def fetch_store_insights(req: StoreRequest):
    try:
        website_url = req.website_url
        if not website_url.startswith("http"):
            website_url = "https://" + website_url

        # ✅ 1. Check DB
        brand_in_db = get_brand_context_from_db(website_url)
        if brand_in_db:
            return brand_in_db

        # ✅ 2. If not in DB → scrape
        brand_name = await scraper.get_brand_name(website_url) 
        products = await scraper.get_product_catalog(website_url) 
        hero_products = await scraper.get_hero_products(website_url) 
        policies = await scraper.get_policies(website_url) 
        faqs = await scraper.get_faqs(website_url) 
        socials = await scraper.get_social_handles(website_url) 
        contact = await scraper.get_contact_details(website_url) 
        about = await scraper.get_about_text(website_url) 
        links = await scraper.get_links(website_url) 

        insights = BrandContext( 
                            brand_name=brand_name, 
                            product_catalog=products, 
                            hero_products=hero_products, 
                            policies=Policy(**policies) if policies else Policy(), 
                            faqs=[FAQ(**f) for f in faqs] if faqs else [], 
                            social_handles=socials, 
                            contact=Contact(**contact) if contact else Contact(), 
                            about=about, 
                            links=Links(**links) if links else Links() )

        # ✅ 3. Save scraped data into DB
        await save_to_db(insights, website_url)

        return insights

    except httpx.HTTPStatusError:
        raise HTTPException(status_code=401, detail="Website not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

