# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary
from sqlalchemy.orm import relationship

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy



class Roles(Base):
    id = Column(Integer, primary_key=True)
    role = Column(String(20), nullable=False)
    description = Column(String(320), nullable=True)

    userroles = relationship("UserRoles", back_populates="roles")

    @classmethod
    def get_id(cls):
        return Roles.id


    FIELDS = {"role": str, "description": str}

    FIELDS.update(Base.FIELDS)
