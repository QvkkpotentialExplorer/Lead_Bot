from datetime import datetime

import pytz
from sqlalchemy import CheckConstraint, String, DateTime, func, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.user import User
from core.models.base import Base

VALID_ACTIONS = ('click_start',
                 'click_get_instruction',
                 'send_notif_guide',
                 'send_notif_instruction',
                 'send_final',
                 'complete_click')


# Преобразуем в нужную временную зону, например, в Московское время


class Action(Base):
    __tablename__ = 'action'
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    type_action: Mapped[str] = mapped_column(String, nullable=False)
    time_action = mapped_column(DateTime)
    __table_args__ = (
        CheckConstraint(type_action.in_(VALID_ACTIONS), name='check_valid_action'),
    )
