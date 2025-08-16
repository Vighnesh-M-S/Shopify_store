from app.db import SessionLocal
from app import models_db

def get_brand_from_db(url: str):
    db = SessionLocal()
    try:
        brand = db.query(models_db.Brand).filter(models_db.Brand.url == url).first()
        return brand
    finally:
        db.close()
