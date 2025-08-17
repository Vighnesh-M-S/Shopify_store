# Shopify_store

## Project Overview
----------------

**Shopify Store Insights** is a FastAPI-based project that extracts detailed information about Shopify stores including brand details, product catalog, policies, contact information, and competitors. This project also allows fetching insights for competitor stores.

The project is designed to:
*   Scrape or fetch store information from databases.    
*   Store the data in MySQL (hosted on Railway).    
*   Deploy the API using Render.    
*   Fetch competitor stores via APIs (SerpAPI / SimilarWeb / other sources).    

## Features
--------

*   Fetch store insights:  
    *   Brand name & about    
    *   Product catalog & hero products        
    *   Policies (privacy & return)        
    *   Contact details (emails, phones, address)        
    *   FAQs & social media handles
    *   Useful links        
*   Fetch competitor stores    
*   Save insights to MySQL for future retrieval    
*   Designed for easy integration with web frontends
    
## Tech Stack
----------

*   Backend: **FastAPI**, **Python**    
*   Database: **MySQL** (Railway)    
*   Deployment: **Render**    
*   HTTP Client: **httpx**    
*   Web Scraping: Custom scraper or APIs (SerpAPI, SimilarWeb)    
*   Asynchronous operations using **asyncio**
    

##APIs
----

### 1\. Fetch Store Insights

**Endpoint:** /fetch\_store\_insights**Method:** POST**Request Body:**
bash 
```
 {    "website_url": "https://example-store.com"  }   
 ```

**Response:**

bash
```
{    "brand_name": "Brand Name",    "about": "Brand description",    "product_catalog": [      {"title": "Product 1", "price": 100, "url": "product-1-url"}    ],    "hero_products": [],    "policies": {"privacy_policy": "...", "return_policy": "..."},    "faqs": [],    "social_handles": {},    "contact": {"emails": [], "phones": [], "address": ""},    "links": {}  }
```

### 2\. Get Competitors

**Endpoint:** /get\_competitors**Method:** POST**Request Body:**
bash
```
{    "website_url": "https://example-store.com",    "competitor_urls": ["https://competitor1.com", "https://competitor2.com"]  // optional  }
```

**Response:**

bash
```
{    "main": "https://example-store.com",    "competitors": ["https://competitor1.com", "https://competitor2.com"]  }
```

## Database
--------

*   **Database:** MySQL (Railway)    
*   **Tables:**    
    *   brands: id, name, url, about        
    *   products: id, title, price, url, brand\_id      
    *   policies: id, privacy\_policy, return\_policy, brand\_id        
    *   contacts: id, emails, phones, address, brand\_id
        

## Deployment
----------

*   **Backend deployed on Render**Enter your deployed URL here:\[https://shopify-store-fv15.onrender.com/]
    
*   **Database hosted on Railway**Database credentials are loaded via .env using DATABASE\_URL
    

Demo
----

*   Demo video:

Uploading Vighnesh ms's explaination.mp4…


    

Setup Instructions
------------------

1.  Clone repository    

bash
```
git clone   cd Shopify_store
```

1.  Create .env file
    

bash
```
DATABASE_URL="mysql+pymysql://user:password@host:port/dbname"  SERPAPI_KEY="your_serpapi_key"  SIMILARWEB_API_KEY="your_similarweb_api_key"
```

1.  Install dependencies
    
bash
```
pip install -r requirements.txt
```

1.  Run migrations / create tables
    

bash
```
from app.db import Base, engine  Base.metadata.create_all(bind=engine)
```

1.  Run the FastAPI server
    
bash
```
uvicorn app.main:app --reload
```

Screenshots
-----------

Include any screenshots of API responses or front-end here.

Notes
-----

*   For competitor fetching, you can use **SerpAPI** or **SimilarWeb** API.
    
*   The scraper is asynchronous and optimized to reduce latency.
    
*   Ensure your .env keys are valid before deployment.
