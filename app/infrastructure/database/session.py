from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.settings import setting



asyncengine = create_async_engine(
    setting.SQLALCHEMY_DATABASE_URL
)

LocalSession = async_sessionmaker(autocommiy=False, autoflush=False, bind=asyncengine)


async def get_session_database():
    db = LocalSession()
    try:
        yield db
    finally:
        await db.close()