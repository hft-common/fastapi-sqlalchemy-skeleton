from sqlalchemy.sql.schema import ForeignKeyConstraint
from sqlalchemy_utils.types.password import PasswordType

from data.db.init_db import ModelBase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship


class Signals(ModelBase):
    __tablename__ = 'signals'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    td_up = Column(Float)
    td_down = Column(Float)
    timestamp = Column(DateTime)  #May be redundant
    ohlc = Column(Integer)

    ForeignKeyConstraint(
        ['ohlc'], ['ohlc_data.id']
    )

