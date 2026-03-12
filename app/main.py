from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
import app.models.user
import app.models.route
import app.models.request_log


app = FastAPI(
    title="API Gateway",
    description="A self-hostable API Gateway with rate limiting",
    version="0.1.0"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway"
    }


