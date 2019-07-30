# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, LargeBinary
from sqlalchemy.orm import relationship

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class UserRoles(Base):

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    role = Column(Integer, ForeignKey('roles.id'))

    user = relationship("User", back_populates="userroles")
    roles = relationship("Roles", back_populates="userroles")


    @classmethod
    def get_id(cls):
        return UserRoles.id

    FIELDS = {user_id: int, "role": int}
    FIELDS.update(Base.FIELDS)
