from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings


Base = declarative_base()
engine = create_async_engine(settings.sqlalchemy_uri, echo=True)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with Session() as session:
        yield session