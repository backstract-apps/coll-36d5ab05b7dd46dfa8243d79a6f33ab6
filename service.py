from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def put_travel(db: Session, raw_data: schemas.PutTravel):
    id: int = raw_data.id
    place: str = raw_data.place
    pincode: str = raw_data.pincode

    query = db.query(models.Travel)
    query = query.filter(and_(models.Travel.id == id))

    user_place = query.first()

    user_place = (
        (user_place.to_dict() if hasattr(user_place, "to_dict") else vars(user_place))
        if user_place
        else user_place
    )

    res = {
        "user_place": user_place,
    }
    return res


async def post_travel(db: Session, raw_data: schemas.PostTravel):
    id: int = raw_data.id
    place: str = raw_data.place
    pincode: str = raw_data.pincode

    record_to_be_added = {"id": id, "place": place, "pincode": pincode}
    new_travel = models.Travel(**record_to_be_added)
    db.add(new_travel)
    db.commit()
    db.refresh(new_travel)
    add_place = new_travel.to_dict()

    query = db.query(models.Travel)
    query = query.filter(and_(models.Travel.id == id))
    edit_records = query.first()

    if edit_records:
        for key, value in {"id": id, "place": pincode, "pincode": place}.items():
            setattr(edit_records, key, value)

        db.commit()
        db.refresh(edit_records)

        edit_records = (
            edit_records.to_dict()
            if hasattr(edit_records, "to_dict")
            else vars(edit_records)
        )

    query = db.query(models.Travel)
    query = query.filter(and_(models.Travel.place == pincode))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        delete_records = record_to_delete.to_dict()
    else:
        delete_records = record_to_delete
    res = {
        "add_place": add_place,
        "edit_records": edit_records,
        "delete_records": delete_records,
    }
    return res


async def get_travel(db: Session, id: int):

    query = db.query(models.Travel)
    query = query.filter(and_(models.Travel.id == id))

    get_record = query.first()

    get_record = (
        (get_record.to_dict() if hasattr(get_record, "to_dict") else vars(get_record))
        if get_record
        else get_record
    )

    res = {
        "get_record": get_record,
    }
    return res


async def get_parking_spaces_id(db: Session, id: int):

    query = db.query(models.ParkingSpaces)
    query = query.filter(and_(models.ParkingSpaces.id == id))

    parking_spaces_one = query.first()

    parking_spaces_one = (
        (
            parking_spaces_one.to_dict()
            if hasattr(parking_spaces_one, "to_dict")
            else vars(parking_spaces_one)
        )
        if parking_spaces_one
        else parking_spaces_one
    )

    try:
        print("Hello")
    except Exception as e:
        raise HTTPException(500, str(e))

    parking_1 = aliased(models.ParkingSpaces)
    query = db.query(models.ParkingSpaces, parking_1)

    query = query.join(
        parking_1, and_(models.ParkingSpaces.id == models.ParkingSpaces.id)
    )

    test = query.all()
    test = (
        [
            {
                "test_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "test_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in test
        ]
        if test
        else test
    )
    res = {
        "parking_spaces_one": parking_spaces_one,
        "test": test,
    }
    return res


async def get_parking_spaces(db: Session):

    query = db.query(models.ParkingSpaces)

    parking_spaces_all = query.all()
    parking_spaces_all = (
        [new_data.to_dict() for new_data in parking_spaces_all]
        if parking_spaces_all
        else parking_spaces_all
    )
    res = {
        "parking_spaces_all": parking_spaces_all,
    }
    return res


async def post_parking_spaces(db: Session, raw_data: schemas.PostParkingSpaces):
    id: int = raw_data.id
    space_number: str = raw_data.space_number
    is_occupied: int = raw_data.is_occupied

    record_to_be_added = {
        "id": id,
        "is_occupied": is_occupied,
        "space_number": space_number,
    }
    new_parking_spaces = models.ParkingSpaces(**record_to_be_added)
    db.add(new_parking_spaces)
    db.commit()
    db.refresh(new_parking_spaces)
    parking_spaces_inserted_record = new_parking_spaces.to_dict()

    res = {
        "parking_spaces_inserted_record": parking_spaces_inserted_record,
    }
    return res


async def put_parking_spaces_id(
    db: Session, id: int, space_number: str, is_occupied: int
):

    query = db.query(models.ParkingSpaces)
    query = query.filter(and_(models.ParkingSpaces.id == id))
    parking_spaces_edited_record = query.first()

    if parking_spaces_edited_record:
        for key, value in {
            "id": id,
            "is_occupied": is_occupied,
            "space_number": space_number,
        }.items():
            setattr(parking_spaces_edited_record, key, value)

        db.commit()
        db.refresh(parking_spaces_edited_record)

        parking_spaces_edited_record = (
            parking_spaces_edited_record.to_dict()
            if hasattr(parking_spaces_edited_record, "to_dict")
            else vars(parking_spaces_edited_record)
        )
    res = {
        "parking_spaces_edited_record": parking_spaces_edited_record,
    }
    return res


async def delete_parking_spaces_id(db: Session, id: int):

    query = db.query(models.ParkingSpaces)
    query = query.filter(and_(models.ParkingSpaces.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        parking_spaces_deleted = record_to_delete.to_dict()
    else:
        parking_spaces_deleted = record_to_delete
    res = {
        "parking_spaces_deleted": parking_spaces_deleted,
    }
    return res


async def get_vehicles(db: Session):

    query = db.query(models.Vehicles)

    vehicles_all = query.all()
    vehicles_all = (
        [new_data.to_dict() for new_data in vehicles_all]
        if vehicles_all
        else vehicles_all
    )
    res = {
        "vehicles_all": vehicles_all,
    }
    return res


async def get_vehicles_id(db: Session, id: int):

    query = db.query(models.Vehicles)
    query = query.filter(and_(models.Vehicles.id == id))

    vehicles_one = query.first()

    vehicles_one = (
        (
            vehicles_one.to_dict()
            if hasattr(vehicles_one, "to_dict")
            else vars(vehicles_one)
        )
        if vehicles_one
        else vehicles_one
    )

    res = {
        "vehicles_one": vehicles_one,
    }
    return res


async def post_vehicles(db: Session, raw_data: schemas.PostVehicles):
    id: int = raw_data.id
    license_plate: str = raw_data.license_plate

    record_to_be_added = {"id": id, "license_plate": license_plate}
    new_vehicles = models.Vehicles(**record_to_be_added)
    db.add(new_vehicles)
    db.commit()
    db.refresh(new_vehicles)
    vehicles_inserted_record = new_vehicles.to_dict()

    res = {
        "vehicles_inserted_record": vehicles_inserted_record,
    }
    return res


async def put_vehicles_id(db: Session, id: int, license_plate: str):

    query = db.query(models.Vehicles)
    query = query.filter(and_(models.Vehicles.id == id))
    vehicles_edited_record = query.first()

    if vehicles_edited_record:
        for key, value in {"id": id, "license_plate": license_plate}.items():
            setattr(vehicles_edited_record, key, value)

        db.commit()
        db.refresh(vehicles_edited_record)

        vehicles_edited_record = (
            vehicles_edited_record.to_dict()
            if hasattr(vehicles_edited_record, "to_dict")
            else vars(vehicles_edited_record)
        )
    res = {
        "vehicles_edited_record": vehicles_edited_record,
    }
    return res


async def delete_vehicles_id(db: Session, id: int):

    query = db.query(models.Vehicles)
    query = query.filter(and_(models.Vehicles.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        vehicles_deleted = record_to_delete.to_dict()
    else:
        vehicles_deleted = record_to_delete
    res = {
        "vehicles_deleted": vehicles_deleted,
    }
    return res


async def get_parking_events(db: Session):

    query = db.query(models.ParkingEvents)

    parking_events_all = query.all()
    parking_events_all = (
        [new_data.to_dict() for new_data in parking_events_all]
        if parking_events_all
        else parking_events_all
    )
    res = {
        "parking_events_all": parking_events_all,
    }
    return res


async def get_parking_events_id(db: Session, id: int):

    query = db.query(models.ParkingEvents)
    query = query.filter(and_(models.ParkingEvents.id == id))

    parking_events_one = query.first()

    parking_events_one = (
        (
            parking_events_one.to_dict()
            if hasattr(parking_events_one, "to_dict")
            else vars(parking_events_one)
        )
        if parking_events_one
        else parking_events_one
    )

    res = {
        "parking_events_one": parking_events_one,
    }
    return res


async def post_parking_events(db: Session, raw_data: schemas.PostParkingEvents):
    id: int = raw_data.id
    vehicle_id: int = raw_data.vehicle_id
    space_id: int = raw_data.space_id
    entry_time: str = raw_data.entry_time
    exit_time: str = raw_data.exit_time

    record_to_be_added = {
        "id": id,
        "space_id": space_id,
        "exit_time": exit_time,
        "entry_time": entry_time,
        "vehicle_id": vehicle_id,
    }
    new_parking_events = models.ParkingEvents(**record_to_be_added)
    db.add(new_parking_events)
    db.commit()
    db.refresh(new_parking_events)
    parking_events_inserted_record = new_parking_events.to_dict()

    res = {
        "parking_events_inserted_record": parking_events_inserted_record,
    }
    return res


async def put_parking_events_id(
    db: Session,
    id: int,
    vehicle_id: int,
    space_id: int,
    entry_time: str,
    exit_time: str,
):

    query = db.query(models.ParkingEvents)
    query = query.filter(and_(models.ParkingEvents.id == id))
    parking_events_edited_record = query.first()

    if parking_events_edited_record:
        for key, value in {
            "id": id,
            "space_id": space_id,
            "exit_time": exit_time,
            "entry_time": entry_time,
            "vehicle_id": vehicle_id,
        }.items():
            setattr(parking_events_edited_record, key, value)

        db.commit()
        db.refresh(parking_events_edited_record)

        parking_events_edited_record = (
            parking_events_edited_record.to_dict()
            if hasattr(parking_events_edited_record, "to_dict")
            else vars(parking_events_edited_record)
        )
    res = {
        "parking_events_edited_record": parking_events_edited_record,
    }
    return res


async def delete_parking_events_id(db: Session, id: int):

    query = db.query(models.ParkingEvents)
    query = query.filter(and_(models.ParkingEvents.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        parking_events_deleted = record_to_delete.to_dict()
    else:
        parking_events_deleted = record_to_delete
    res = {
        "parking_events_deleted": parking_events_deleted,
    }
    return res


async def post_file_upload(db: Session, document: UploadFile):

    bucket_name = "ap-south-1"
    region_name = "TATDR8Mj+m+Le01qH6zzkdAHbZU6MTczw2EX5nDX"
    file_path = "resources"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id="AKIATET5D5CP6X5H4BNH",
        aws_secret_access_key="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",
        aws_session_token=None,  # Optional, can be removed if not used
        region_name="TATDR8Mj+m+Le01qH6zzkdAHbZU6MTczw2EX5nDX",
    )

    # Read file content
    file_content = await document.read()

    name = document.filename
    file_path = file_path + "/" + name

    import mimetypes

    document.file.seek(0)

    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    s3_client.upload_fileobj(
        document.file, bucket_name, name, ExtraArgs={"ContentType": content_type}
    )

    file_type = Path(document.filename).suffix
    file_size = 200

    file_url = f"https://{bucket_name}.s3.amazonaws.com/{name}"

    vbhmnkbnm = file_url
    res = {
        "user_upload_file_details": vbhmnkbnm,
    }
    return res
