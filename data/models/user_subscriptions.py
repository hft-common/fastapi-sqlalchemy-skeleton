from sqlalchemy.sql.schema import ForeignKeyConstraint
from sqlalchemy_utils.types.password import PasswordType

from data.db.init_db import ModelBase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship


class UserSubscriptions(ModelBase):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user = Column(Integer)
    ticker = Column(String)
    timeframe = Column(String)

    __table_args__ = (
        ForeignKeyConstraint(
            ('ticker', 'timeframe'),
            ['subscriptions.ticker', 'subscriptions.timeframe']
        ),
    )
