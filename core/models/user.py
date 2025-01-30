from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.models.base import Base


class User(Base):
    __tablename__ = 'user'

    tg_id: Mapped[int]
    username: Mapped[str]
    account_url: Mapped[str]
    phone: Mapped[str]
    send_notification = mapped_column(Boolean,default=False)
    send_second_notification = mapped_column(Boolean,default=False)
    is_first_instruction = mapped_column(Boolean,default=False)

    get_consult =  mapped_column(Boolean,default=False)
    get_free_consult = mapped_column(Boolean,default=False)
    get_free_description = mapped_column(Boolean,default=False)
    is_sub = mapped_column(Boolean,default=False)
    send_full = mapped_column(Boolean,default=False)
