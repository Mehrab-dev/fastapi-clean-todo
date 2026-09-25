from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.settings import setting


engine = create_async_engine(
    setting.SQLALCHEMY_DATABASE_URL
)

sessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_database_session():
    db = sessionLocal()
    try:
        yield db
    finally:
        await db.close()
