"""Business logic for vehicles and stock."""
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleUpdate


class VehicleNotFound(Exception):
    pass


def get_vehicle(db: Session, vehicle_id: int) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise VehicleNotFound(vehicle_id)
    return vehicle


def list_vehicles(db: Session) -> list[Vehicle]:
    return list(db.scalars(select(Vehicle).order_by(Vehicle.id)))


def search_vehicles(
    db: Session,
    make: str | None = None,
    model: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[Vehicle]:
    # Start with "all vehicles" and narrow it down with each filter that was given.
    query = select(Vehicle)
    if make:
        query = query.where(Vehicle.make.ilike(f"%{make}%"))
    if model:
        query = query.where(Vehicle.model.ilike(f"%{model}%"))
    if category:
        query = query.where(Vehicle.category.ilike(category))
    if min_price is not None:
        query = query.where(Vehicle.price >= min_price)
    if max_price is not None:
        query = query.where(Vehicle.price <= max_price)
    return list(db.scalars(query.order_by(Vehicle.id)))


def create_vehicle(db: Session, data: VehicleCreate) -> Vehicle:
    vehicle = Vehicle(**data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def update_vehicle(db: Session, vehicle_id: int, changes: VehicleUpdate) -> Vehicle:
    vehicle = get_vehicle(db, vehicle_id)
    for field, value in changes.model_dump(exclude_unset=True).items():
        setattr(vehicle, field, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete_vehicle(db: Session, vehicle_id: int) -> None:
    db.delete(get_vehicle(db, vehicle_id))
    db.commit()