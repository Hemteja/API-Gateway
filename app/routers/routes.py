from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.route import Route
from app.schemas.route import RouteCreate, RouteResponse
from typing import List

router = APIRouter(prefix="/routes", tags=["routes"])

@router.post("/", response_model=RouteResponse)
def register_route(
    route: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_route = db.query(Route).filter(Route.name == route.name).first()
    if existing_route:
        raise HTTPException(status_code=400, detail="Route name already exists")

    new_route = Route(
        name=route.name,
        target_url=route.target_url,
        rate_limit=route.rate_limit,
        rate_limit_window=route.rate_limit_window,
        user_id=current_user.id
    )
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route

@router.get("/", response_model=List[RouteResponse])
def get_routes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    routes = db.query(Route).filter(Route.user_id == current_user.id).all()
    return routes

@router.delete("/{route_id}")
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    route = db.query(Route).filter(
        Route.id == route_id,
        Route.user_id == current_user.id
    ).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    db.delete(route)
    db.commit()
    return {"message": "Route deleted successfully"}
