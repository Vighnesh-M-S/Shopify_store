import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import urllib.parse

# Load .env file
load_dotenv()

def get_database_url():
    """Handle both direct URL and Render-style environment variables"""
    if os.getenv("DATABASE_URL"):
        # Parse and ensure proper MySQL format
        url = urllib.parse.urlparse(os.getenv("DATABASE_URL"))
        if url.scheme == 'mysql':
            return f"mysql+pymysql://{url.username}:{url.password}@{url.hostname}:{url.port}{url.path}"
        return os.getenv("DATABASE_URL")
    
    # Fallback to individual components (Render-style)
    return (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

DATABASE_URL = get_database_url()

if not DATABASE_URL:
    raise ValueError(
        "Database connection not configured. "
        "Please set either DATABASE_URL or individual DB_* variables"
    )

# Configure engine with additional settings for production
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
    pool_timeout=30,
    connect_args={
        "connect_timeout": 5,
        "ssl": {"ssl_ca": "/etc/ssl/cert.pem"}  # For secure connections
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()