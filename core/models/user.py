from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.models.base import Base


class User(Base):
    __tablename__ = 'user'

    tg_id: Mapped[int]
    username: Mapped[str]
    account_url: Mapped[str]
    phone: Mapped[str]
    send_final = mapped_column(Boolean,default=False)
