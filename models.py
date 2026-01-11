from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from database import Base

class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String(50), nullable=False)
    room_uuid = Column(String(100), unique=True, nullable=False)

    anchor_pos_x = Column(Float, nullable=True)
    anchor_pos_y = Column(Float, nullable=True)
    anchor_pos_z = Column(Float, nullable=True)

    anchor_rot_x = Column(Float, nullable=True)
    anchor_rot_y = Column(Float, nullable=True)
    anchor_rot_z = Column(Float, nullable=True)
    anchor_rot_w = Column(Float, nullable=True)

    created_at = Column(TIMESTAMP)



class ObjectMemory(Base):
    __tablename__ = "object_memory"

    object_id = Column(Integer, primary_key=True, index=True)
    object_name = Column(String(50), nullable=False)
    object_tag = Column(String(50), unique=True, nullable=False)

    current_room_id = Column(Integer, ForeignKey("rooms.room_id"))
    posX = Column(Float)
    posY = Column(Float)
    posZ = Column(Float)

