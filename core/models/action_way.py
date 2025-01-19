
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.user import User
from core.models.base import Base


class ActionWay(Base):
    __tablename__ = 'action_way'
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    start_click: Mapped[bool] = mapped_column(Boolean, default=True)
    get_instruct: Mapped[bool] = mapped_column(Boolean, default=False)
    get_complete: Mapped[bool] = mapped_column(Boolean, default=False)
