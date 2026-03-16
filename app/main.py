from fastapi import FastAPI, Depends
from app.db.session import engine
from app.db.base import Base
import app.models.user
import app.models.route
import app.models.request_log
from app.routers import auth
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.routers import auth, routes


app = FastAPI(
    title="API-Gateway",
    description="A self-hostable API Gateway with rate limiting",
    version="0.1.0"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(auth.router)
app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway"
    }

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user.email}",
        "user_id": current_user.id
    }
