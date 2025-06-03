from pydantic import BaseModel

import datetime

import uuid

from typing import Any, Dict, List, Tuple

class ParkingSpaces(BaseModel):
    id: Any
    space_number: str
    is_occupied: int


class ReadParkingSpaces(BaseModel):
    id: Any
    space_number: str
    is_occupied: int
    class Config:
        from_attributes = True


class Vehicles(BaseModel):
    id: Any
    license_plate: str


class ReadVehicles(BaseModel):
    id: Any
    license_plate: str
    class Config:
        from_attributes = True


class ParkingEvents(BaseModel):
    id: Any
    vehicle_id: int
    space_id: int
    entry_time: Any
    exit_time: Any


class ReadParkingEvents(BaseModel):
    id: Any
    vehicle_id: int
    space_id: int
    entry_time: Any
    exit_time: Any
    class Config:
        from_attributes = True


class Travel(BaseModel):
    id: int
    place: str
    pincode: str


class ReadTravel(BaseModel):
    id: int
    place: str
    pincode: str
    class Config:
        from_attributes = True




class PutTravel(BaseModel):
    id: int
    place: str
    pincode: str

    class Config:
        from_attributes = True



class PostTravel(BaseModel):
    id: int
    place: str
    pincode: str

    class Config:
        from_attributes = True



class PostParkingSpaces(BaseModel):
    id: int
    space_number: str
    is_occupied: int

    class Config:
        from_attributes = True



class PostVehicles(BaseModel):
    id: int
    license_plate: str

    class Config:
        from_attributes = True



class PostParkingEvents(BaseModel):
    id: int
    vehicle_id: int
    space_id: int
    entry_time: str
    exit_time: str

    class Config:
        from_attributes = True

