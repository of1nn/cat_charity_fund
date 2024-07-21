from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.base import BaseModel
from app.core.db import Base


class Donation(BaseModel, Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
