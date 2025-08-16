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

async def get_policies(base_url: str):
    """Scrape Privacy and Return/Refund policies"""
    try:
        html = await fetch_page(base_url)
        soup = BeautifulSoup(html, "lxml")
        privacy, returns = None, None

        for a in soup.find_all("a", href=True):
            link = a["href"].lower()
            if "privacy" in link:
                privacy = base_url + a["href"] if not a["href"].startswith("http") else a["href"]
            if "return" in link or "refund" in link:
                returns = base_url + a["href"] if not a["href"].startswith("http") else a["href"]

        return {"privacy_policy": privacy, "return_policy": returns}
    except:
        return {"privacy_policy": None, "return_policy": None}


async def get_faqs(base_url: str):
    """Scrape FAQs (naive approach – looks for 'faq' page and extracts Q/A)"""
    try:
        html = await fetch_page(base_url)
        soup = BeautifulSoup(html, "lxml")
        faq_url = None

        for a in soup.find_all("a", href=True):
            if "faq" in a["href"].lower():
                faq_url = a["href"]
                if not faq_url.startswith("http"):
                    faq_url = base_url + faq_url
                break

        if not faq_url:
            return []

        faq_html = await fetch_page(faq_url)
        faq_soup = BeautifulSoup(faq_html, "lxml")

        faqs = []
        for q in faq_soup.find_all(["h2", "h3"]):
            text = q.get_text(strip=True)
            if text.endswith("?"):
                ans = q.find_next("p").get_text(strip=True) if q.find_next("p") else ""
                faqs.append({"question": text, "answer": ans})
        return faqs
    except:
        return []


async def get_social_handles(base_url: str):
    """Extract social media links"""
    try:
        html = await fetch_page(base_url)
        soup = BeautifulSoup(html, "lxml")
        socials = {}
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "instagram.com" in href:
                socials["instagram"] = href
            if "facebook.com" in href:
                socials["facebook"] = href
            if "tiktok.com" in href:
                socials["tiktok"] = href
        return socials
    except:
        return {}


async def get_contact_details(base_url: str):
    """Extract emails and phone numbers from Contact page"""
    try:
        html = await fetch_page(base_url)
        soup = BeautifulSoup(html, "lxml")

        # Find a "contact" page link
        contact_url = None
        for a in soup.find_all("a", href=True):
            if "contact" in a["href"].lower():
                contact_url = a["href"]
                if not contact_url.startswith("http"):
                    contact_url = base_url + contact_url
                break

        if not contact_url:
            return {"emails": [], "phones": []}

        contact_html = await fetch_page(contact_url)
        text = BeautifulSoup(contact_html, "lxml").get_text(" ")

        emails = list(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)))
        phones = list(set(re.findall(r"\+?\d[\d -]{8,}\d", text)))

        return {"emails": emails, "phones": phones}
    except:
        return {"emails": [], "phones": []}


async def get_about_text(base_url: str):
    """Extract About Us section"""
    try:
        html = await fetch_page(base_url)
        soup = BeautifulSoup(html, "lxml")

        about_url = None
        for a in soup.find_all("a", href=True):
            if "about" in a["href"].lower():
                about_url = a["href"]
                if not about_url.startswith("http"):
                    about_url = base_url + about_url
                break

        if not about_url:
            return None

        about_html = await fetch_page(about_url)
        about_soup = BeautifulSoup(about_html, "lxml")
        return about_soup.get_text(" ", strip=True)[:1000]  # limit
    except:
        return None


async def get_links(base_url: str):
    """Extract important links (order tracking, blogs, contact)"""
    try:
        html = await fetch_page(base_url)
        soup = BeautifulSoup(html, "lxml")
        links = {}

        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True).lower()
            href = a["href"].lower()
            full_url = base_url + a["href"] if not a["href"].startswith("http") else a["href"]

            # Order Tracking - check both href + text
            if ("order" in href and "track" in href) or ("track my order" in text) or ("order tracking" in text):
                links["order_tracking"] = full_url

            # Contact page
            if "contact" in href or "contact" in text:
                links["contact_us"] = full_url

            # Blog page
            if "blog" in href or "blog" in text:
                links["blogs"] = full_url

        return links
    except Exception:
        return {}
