from fastapi import FastAPI
from app.routers import insights
import uvicorn

app = FastAPI(title="Shopify Insights API")

app.include_router(insights.router)

if __name__ == "__main__":
	uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
