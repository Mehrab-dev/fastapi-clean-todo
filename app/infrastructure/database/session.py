
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.configs import setting


async_engine = create_async_engine(
    setting.SQLALCHEMY_DATABASE_URL
)

AsyncLocalSession = async_sessionmaker(autoflush=False, expire_on_commit=False, bind=async_engine)

async def get_database_session():
    async with AsyncLocalSession() as session:
        yield session