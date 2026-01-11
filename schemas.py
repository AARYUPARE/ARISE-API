from pydantic import BaseModel

class RoomCreate(BaseModel):
    room_name: str
    room_uuid: str

class RoomResponse(BaseModel):
    room_id: int
    room_name: str
    room_uuid: str

    class Config:
        orm_mode = True
from pydantic import BaseModel
from typing import List
from datetime import datetime

class ObjectDTO(BaseModel):
    object_id: int
    object_name: str
    object_tag: str
    posX: float
    posY: float
    posZ: float

    class Config:
        orm_mode = True

class ObjectCreate(BaseModel):
    object_name: str
    object_tag: str
    current_room_id: int
    posX: float
    posY: float
    posZ: float

class RoomFullDTO(BaseModel):
    room_id: int
    room_name: str
    room_uuid: str
    objects: List[ObjectDTO]

    class Config:
        orm_mode = True

class RoomAnchorUpdate(BaseModel):
    anchor_pos_x: float
    anchor_pos_y: float
    anchor_pos_z: float
    anchor_rot_x: float
    anchor_rot_y: float
    anchor_rot_z: float
    anchor_rot_w: float