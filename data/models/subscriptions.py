from sqlalchemy_utils.types.password import PasswordType

from data.db.init_db import ModelBase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship



class Subscriptions(ModelBase):
    __tablename__ = "subscriptions"

    ticker = Column(String, primary_key=True)
    timeframe = Column(String, primary_key=True)

