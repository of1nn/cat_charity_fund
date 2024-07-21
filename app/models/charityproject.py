from sqlalchemy import Column, Text, String

from app.models.base import BaseModel
from app.core.db import Base


class CharityProject(BaseModel, Base):
    name = Column(String(100), nullable=False, unique=True)
    text = Column(Text, nullable=False)
