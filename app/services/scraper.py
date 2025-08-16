import httpx
from bs4 import BeautifulSoup
import re

async def fetch_page(url: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=15)
        resp.raise_for_status()
        return resp.text

async def get_product_catalog(base_url: str):
    """Fetch products from /products.json endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{base_url}/products.json", timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("products", [])
    except Exception:
        return []
    return []

async def get_hero_products(base_url: str):
    """Scrape home page for featured products"""
    try:
        html = await fetch_page(base_url)
        soup = BeautifulSoup(html, "lxml")
        hero = []
        for product in soup.select("a[href*='/products/']"):
            name = product.get_text(strip=True)
            link = product.get("href")
            if name and link:
                hero.append({"name": name, "url": base_url + link})
        return hero[:5]  # take top few
    except Exception:
        return []

async def get_brand_name(base_url: str):
    """Get title/brand name"""
    try:
        html = await fetch_page(base_url)
        soup = BeautifulSoup(html, "lxml")
        return soup.title.string if soup.title else None
    except Exception:
        return None