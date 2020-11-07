import sys
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from functools import wraps

from common.domain.entity import EntityMap
from common.event import Event, EventBus
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import sessionmaker


class AbstractUnitOfWork(ABC):

    def __init__(self, event_bus: EventBus) -> None:
        self.__event_bus = event_bus
        self.__events: list[Event] = list()

    def emit_event(self, event: Event) -> None:
        if not self.__event_bus:
            raise RuntimeError("This unit of work cannot emit events")
        self.__events.append(event)

    @abstractmethod
    async def commit(self) -> None:
        pass

    async def after_successful_transaction(self) -> None:
        await self.__publish_events()

    @abstractmethod
    async def rollback(self) -> None:
        self.__events.clear()

    async def __publish_events(self) -> None:
        if self.__event_bus:
            await self.__event_bus.post_events(self.__events)
            self.__events.clear()


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self, event_bus: EventBus, session: Session) -> None:
        super().__init__(event_bus=event_bus)
        self.__session = session
        self.__detached_entity_map = EntityMap()

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def detached_entity_map(self) -> EntityMap:
        return self.__detached_entity_map

    async def commit(self) -> None:
        await self.__session.commit()

    async def rollback(self) -> None:
        await self.__session.rollback()
        self.__detached_entity_map = EntityMap()
        await super().rollback()


@asynccontextmanager
async def make_unit_of_work(async_session_maker: sessionmaker) -> AsyncGenerator[UnitOfWork, None]:
    uow: UnitOfWork
    async with async_session_maker() as session:
        try:
            application_module = sys.modules["application"]
            event_bus = application_module.get_dependency(EventBus)  # type: ignore
            uow = UnitOfWork(event_bus=event_bus, session=session)
            await uow.rollback()  # Force initial rollback to ensure hanging operations are killed
            async with session.begin():
                yield uow
            await uow.commit()
        except BaseException:
            await uow.rollback()
            raise

    await uow.after_successful_transaction()


def unit_of_work(coroutine):
    @wraps(coroutine)
    async def new_coroutine(self, *args, **kwargs):
        if kwargs.get('uow'):
            return await coroutine(self, *args, **kwargs)

        async with make_unit_of_work(self.repository_utils.sessionmaker) as uow:
            res = await coroutine(self, *args, **kwargs, uow=uow)

        return res

    return new_coroutine
