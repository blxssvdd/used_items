from uuid import uuid4
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext
import jwt

from app.config import settings
from app.db.base import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password_: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, pwd):
        self.password_ = pwd_context.hash(pwd)

    def is_verify_password(self, pwd):
        return pwd_context.verify(pwd, self.password_)


    def create_token(self, expires_delta: int = settings.access_token_expire_minutes):
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
        payload = dict(sub=self.username, exp=expire)
        token = jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algorithm)
        return dict(access_token=token, token_type="Bearer")


