from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
import service, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put('/travel')
async def put_travel(raw_data: schemas.PutTravel, db: Session = Depends(get_db)):
    try:
        return await service.put_travel(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/travel')
async def post_travel(raw_data: schemas.PostTravel, db: Session = Depends(get_db)):
    try:
        return await service.post_travel(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/travel')
async def get_travel(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_travel(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/parking_spaces/id')
async def get_parking_spaces_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_parking_spaces_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/parking_spaces/')
async def get_parking_spaces(db: Session = Depends(get_db)):
    try:
        return await service.get_parking_spaces(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/parking_spaces/')
async def post_parking_spaces(raw_data: schemas.PostParkingSpaces, db: Session = Depends(get_db)):
    try:
        return await service.post_parking_spaces(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/parking_spaces/id/')
async def put_parking_spaces_id(id: int, space_number: str, is_occupied: int, db: Session = Depends(get_db)):
    try:
        return await service.put_parking_spaces_id(db, id, space_number, is_occupied)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/parking_spaces/id')
async def delete_parking_spaces_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_parking_spaces_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/vehicles/')
async def get_vehicles(db: Session = Depends(get_db)):
    try:
        return await service.get_vehicles(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/vehicles/id')
async def get_vehicles_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_vehicles_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/vehicles/')
async def post_vehicles(raw_data: schemas.PostVehicles, db: Session = Depends(get_db)):
    try:
        return await service.post_vehicles(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/vehicles/id/')
async def put_vehicles_id(id: int, license_plate: str, db: Session = Depends(get_db)):
    try:
        return await service.put_vehicles_id(db, id, license_plate)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/vehicles/id')
async def delete_vehicles_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_vehicles_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/parking_events/')
async def get_parking_events(db: Session = Depends(get_db)):
    try:
        return await service.get_parking_events(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/parking_events/id')
async def get_parking_events_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_parking_events_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/parking_events/')
async def post_parking_events(raw_data: schemas.PostParkingEvents, db: Session = Depends(get_db)):
    try:
        return await service.post_parking_events(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/parking_events/id/')
async def put_parking_events_id(id: int, vehicle_id: int, space_id: int, entry_time: str, exit_time: str, db: Session = Depends(get_db)):
    try:
        return await service.put_parking_events_id(db, id, vehicle_id, space_id, entry_time, exit_time)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/parking_events/id')
async def delete_parking_events_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_parking_events_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/file_upload')
async def post_file_upload(document: UploadFile, db: Session = Depends(get_db)):
    try:
        return await service.post_file_upload(db, document)
    except Exception as e:
        raise HTTPException(500, str(e))

