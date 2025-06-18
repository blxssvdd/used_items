from uuid import uuid4
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from passlib.context import CryptContext
import jwt


from app.config import settings


Base = declarative_base()
engine = create_async_engine(settings.sqlalchemy_uri, echo=True)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
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


        def create_token(self, expires_delta: int = settings.acces_token_expire_minutes  ):
            expire = datetime.now(timezone.utc) + expires_delta
            payload = dict(sub=self.username, exp=expire)
            return jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algorithm)



async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metafata.drop_all)
        await conn.run_sync(Base.metafata.create_all)

async def get_db():
    async with Session() as session:
        yield session