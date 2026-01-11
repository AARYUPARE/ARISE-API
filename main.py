from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Room, ObjectMemory
from schemas import RoomCreate, RoomResponse
from typing import List
from fastapi import HTTPException
from schemas import RoomFullDTO, RoomAnchorUpdate,ObjectCreate
from database import engine
from models import Base
from datetime import datetime

app = FastAPI(title="Memory Anchor API")

Base.metadata.create_all(bind=engine)


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ➕ Add Room
@app.post("/rooms")
def add_room(room: RoomCreate, db: Session = Depends(get_db)):
    new_room = Room(
        room_name=room.room_name,
        room_uuid=room.room_uuid
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return {
        "room_id": new_room.room_id,
        "room_name": new_room.room_name,
        "room_uuid": new_room.room_uuid
    }

# 📥 Get All Rooms
@app.get("/rooms", response_model=List[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@app.get("/rooms/{room_id}/full", response_model=RoomFullDTO)
def get_room_full(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.room_id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    objects = (
        db.query(ObjectMemory)
        .filter(ObjectMemory.current_room_id == room_id)
        .all()
    )

    return {
        "room_id": room.room_id,
        "room_name": room.room_name,
        "room_uuid": room.room_uuid,
        "objects": objects
    }

@app.put("/rooms/{room_id}/anchor")
def update_room_anchor(
    room_id: int,
    anchor: RoomAnchorUpdate,
    db: Session = Depends(get_db)
):
    room = db.query(Room).filter(Room.room_id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    room.anchor_pos_x = anchor.anchor_pos_x
    room.anchor_pos_y = anchor.anchor_pos_y
    room.anchor_pos_z = anchor.anchor_pos_z

    room.anchor_rot_x = anchor.anchor_rot_x
    room.anchor_rot_y = anchor.anchor_rot_y
    room.anchor_rot_z = anchor.anchor_rot_z
    room.anchor_rot_w = anchor.anchor_rot_w

    db.commit()

    return {"status": "anchor_saved"}

@app.post("/objects")
def add_or_update_object(obj: ObjectCreate, db: Session = Depends(get_db)):
    existing_object = (
        db.query(ObjectMemory)
        .filter(ObjectMemory.object_tag == obj.object_tag)
        .first()
    )

    # 🔁 CASE 1: Object already exists → UPDATE
    if existing_object:
        existing_object.object_name = obj.object_name
        existing_object.current_room_id = obj.current_room_id
        existing_object.posX = obj.posX
        existing_object.posY = obj.posY
        existing_object.posZ = obj.posZ

        # ✅ FIX: update timestamp manually

        db.commit()
        db.refresh(existing_object)

        return {
            "object_id": existing_object.object_id,
            "status": "object_updated"
        }

    # ➕ CASE 2: New object → INSERT
    new_object = ObjectMemory(
        object_name=obj.object_name,
        object_tag=obj.object_tag,
        current_room_id=obj.current_room_id,
        posX=obj.posX,
        posY=obj.posY,
        posZ=obj.posZ
    )

    db.add(new_object)
    db.commit()
    db.refresh(new_object)

    return {
        "object_id": new_object.object_id,
        "status": "object_created"
    }


@app.get("/objects/tags")
def get_all_object_tags(db: Session = Depends(get_db)):
    tags = db.query(ObjectMemory.object_tag).all()

    # Flatten list of tuples → list of strings
    return [tag[0] for tag in tags]
