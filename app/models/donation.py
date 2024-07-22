from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.base import BaseModel
from app.core.db import Base


class Donation(BaseModel, Base):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
    )
    comment = Column(Text)
