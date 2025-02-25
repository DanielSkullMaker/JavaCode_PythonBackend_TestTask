import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.core.config import settings


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                     default=uuid.uuid4)


engine = create_async_engine(settings.DATABASE_URL, isolation_level="SERIALIZABLE")
async_session_maker = async_sessionmaker(engine)


async def get_async_session():
    """
    Создает асинхронную сессию для работы с базой данных
    return: async_session_maker: Асинхронная сессия SQLAlchemy
    """
    async with async_session_maker() as async_session:
        yield async_session
