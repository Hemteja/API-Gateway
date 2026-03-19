from fastapi import APIRouter, HTTPException, Request, Response
from sqlalchemy.orm import Session
from fastapi import Depends
from app.auth.dependencies import get_db
from app.models.route import Route
from app.models.request_log import RequestLog
import httpx

router = APIRouter(prefix="/gateway", tags=["gateway"])

@router.api_route("/{route_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_handler(
    route_name: str,
    path: str,
    request: Request,
    db: Session = Depends(get_db)
):
    # Step 1: Look up route in DB
    route = db.query(Route).filter(Route.name == route_name).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Step 2: Build target URL
    target_url = f"{route.target_url}/{path}"

    # Step 3: Forward request to target
    async with httpx.AsyncClient() as client:
        try:
            headers = dict(request.headers)
            headers["user-agent"] = "Mozilla/5.0"
            headers.pop("host", None)

            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body()
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Error connecting to upstream service")

    # Step 4: Log the request
    log = RequestLog(
        route_id=route.id,
        status_code=response.status_code,
        was_blocked=False
    )
    db.add(log)
    db.commit()

    # Step 5: Return response
    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type")
    )
