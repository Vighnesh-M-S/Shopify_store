import httpx
from bs4 import BeautifulSoup
import urllib.parse

async def find_competitors(base_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://www.similarweb.com/website/{base_url}/")
        soup = BeautifulSoup(response.text, 'html.parser')
        return [a['href'] for a in soup.select('.similarweb-container a')]


# async def find_competitors(base_url: str, limit: int = 5):
#     """
#     Finds competitor stores by scraping Google search results.

#     NOTE: Direct scraping of Google is unreliable due to anti-bot measures and
#     frequent changes in their HTML structure. For production use, a dedicated
#     Google Search API service is recommended.

#     Args:
#         base_url: The base domain to find competitors for (e.g., "example.com").
#         limit: The maximum number of competitor URLs to return.

#     Returns:
#         A list of competitor URLs, or an empty list if an error occurs.
#     """
#     # Using a search query that explicitly asks for competitors on Shopify
#     query = f"{base_url} competitors site:shopify.com"
    
#     # Headers to mimic a real browser, reducing the chance of being blocked
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
#     }

#     try:
#         async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
#             resp = await client.get("https://www.google.com/search", params={"q": query}, timeout=15)
#             resp.raise_for_status()  # Raise an exception for bad status codes (e.g., 404, 500)

#             soup = BeautifulSoup(resp.text, "lxml")
#             links = []
            
#             # REPAIRED: Use a more specific selector to target only main search result links.
#             # Google's class for this container is currently 'yuRUbf', but it can change.
#             for link_tag in soup.select("div.yuRUbf > a"):
#                 href = link_tag.get("href")
                
#                 # Google search result links are often relative and need a base
#                 if href and href.startswith("/url?q="):
#                     # Extract the URL from the query parameter
#                     raw_url = href.split("/url?q=")[1].split("&")[0]

#                     # REPAIRED: Decode URL-encoded characters (e.g., %3D -> =, %2F -> /)
#                     clean_url = urllib.parse.unquote(raw_url)
                    
#                     # REPAIRED: Add filters to ensure it's a valid link, not the original site, and not a duplicate
#                     if clean_url.startswith("http") and base_url not in clean_url and clean_url not in links:
#                         links.append(clean_url)
                
#                 if len(links) >= limit:
#                     break
#             return links

#     except httpx.RequestError as e:
#         print(f"🚨 An HTTP request error occurred: {e}")
#         return []
#     except Exception as e:
#         print(f"🚨 An unexpected error occurred: {e}")
#         return []