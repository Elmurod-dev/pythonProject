from datetime import datetime
from tabnanny import check

from sqlalchemy import String, DECIMAL, select, DateTime, TEXT, CHAR, BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from db import Base
from db.utils import CreatedModel
from sqlalchemy.ext.declarative import declarative_base



class User(CreatedModel):
    __tablename__= "users"
    full_name: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    jinsi: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime] = mapped_column(DateTime)
    lang: Mapped[[str]] = mapped_column(CHAR(2))
    phone_number: Mapped[[str]] = mapped_column(String(13))
    user_id: Mapped[BigInteger] = mapped_column(BigInteger)


class Market(CreatedModel):
    __tablename__= "market"
    name : Mapped[str] = mapped_column(String(255))
    city : Mapped[str] = mapped_column(String(255))
    address : Mapped[str] = mapped_column(TEXT)
    description : Mapped[str] = mapped_column(TEXT)

class Message_to_admin(CreatedModel):
    __tablename__= "messages"
    text : Mapped[str] = mapped_column(TEXT)







metadata = Base.metadata

