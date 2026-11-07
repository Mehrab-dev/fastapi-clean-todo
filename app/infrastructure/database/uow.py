
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interface.uow import UnitOfWork



class SqlalchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def commit(self) -> None:
        await self.session.commit()


    async def rollback(self) -> None:
        await self.session.rollback()


    async def __aenter__(self) -> "SqlalchemyUnitOfWork":
        return self


    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None:
            await self.session.rollback()