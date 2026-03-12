from fastapi import FastAPI

app = FastAPI(
    title="API Gateway",
    description="A self-hostable API Gateway with rate limiting",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway"
    }


