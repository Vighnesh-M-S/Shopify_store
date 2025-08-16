from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import insights
import uvicorn


app = FastAPI(title="Shopify Insights API")

# Enable CORS for all origins (customize as needed)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


app.include_router(insights.router)

# Serve index.html at root
@app.get("/", response_class=HTMLResponse)
async def serve_index():
	return FileResponse("index.html")

if __name__ == "__main__":
	uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
