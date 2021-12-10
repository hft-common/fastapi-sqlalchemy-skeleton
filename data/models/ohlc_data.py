from sqlalchemy.sql.schema import ForeignKeyConstraint
from sqlalchemy_utils.types.password import PasswordType

from data.db.init_db import ModelBase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from . import subscriptions


class OhlcData(ModelBase):
    __tablename__ = "ohlc_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    timestamp = Column(DateTime)
    ticker = Column(String)
    timeframe = Column(String)

    __table_args__ = (
        ForeignKeyConstraint(
            ('ticker', 'timeframe'),
            ['subscriptions.ticker', 'subscriptions.timeframe']
        ),
    )
