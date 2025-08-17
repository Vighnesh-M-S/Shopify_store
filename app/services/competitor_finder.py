import os
from serpapi import GoogleSearch
import asyncio
import httpx


SERPAPI_KEY = os.getenv("SERPAPI_KEY")  # get your key from serpapi.com



async def find_competitors(base_url: str, limit: int = 5):
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    if not SERPAPI_KEY:
        raise RuntimeError("SERPAPI_KEY not set")

    url = "https://serpapi.com/search.json"
    query = f"{base_url} site:shopify.com"
    params = {"q": query, "api_key": SERPAPI_KEY, "num": limit}

    links = []
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        for res in data.get("organic_results", []):
            link = res.get("link")
            if link and base_url not in link and link not in links:
                links.append(link)
            if len(links) >= limit:
                break

    except Exception as e:
        print(f"⚠️ SerpAPI request failed: {e}")

    # ✅ Fallback: if no competitors found, return backup list
    if not links:
        links = [
            "https://www.beyoung.in",
            "https://www.snitch.co.in",
            "https://www.freakins.com",
            
        ][:limit]

    return links