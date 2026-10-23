"""Vehicle and inventory endpoints. Every route here requires a logged-in user."""
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas import RestockRequest, VehicleCreate, VehicleOut, VehicleUpdate
from app.services import vehicle_service as service

router = APIRouter(
    prefix="/api/vehicles",
    tags=["vehicles"],
    dependencies=[Depends(get_current_user)],  # protects the whole router
)


def not_found():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")


@router.post("", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
def add_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    return service.create_vehicle(db, data)


@router.get("", response_model=list[VehicleOut])
def list_vehicles(db: Session = Depends(get_db)):
    return service.list_vehicles(db)


# Declared before any "/{id}" GET route so "search" isn't mistaken for an id.
@router.get("/search", response_model=list[VehicleOut])
def search_vehicles(
    make: str | None = None,
    model: str | None = None,
    category: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
):
    return service.search_vehicles(db, make, model, category, min_price, max_price)


@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(vehicle_id: int, changes: VehicleUpdate, db: Session = Depends(get_db)):
    try:
        return service.update_vehicle(db, vehicle_id, changes)
    except service.VehicleNotFound:
        raise not_found()


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    try:
        service.delete_vehicle(db, vehicle_id)
    except service.VehicleNotFound:
        raise not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# ---------- Inventory (added in TDD cycle 4) ----------

@router.post("/{vehicle_id}/purchase", response_model=VehicleOut)
def purchase_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    try:
        return service.purchase_vehicle(db, vehicle_id)
    except service.VehicleNotFound:
        raise not_found()
    except service.OutOfStock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle is out of stock")


@router.post("/{vehicle_id}/restock", response_model=VehicleOut, dependencies=[Depends(require_admin)])
def restock_vehicle(vehicle_id: int, body: RestockRequest, db: Session = Depends(get_db)):
    try:
        return service.restock_vehicle(db, vehicle_id, body.amount)
    except service.VehicleNotFound:
        raise not_found()