from sqlalchemy import BigInteger, String, ForeignKey, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///db-pivaldi.sqlite3')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(String)
    win = Column(Integer, default=0)
    lose = Column(Integer, default=0)
    name: Mapped[str] = mapped_column(String, default="Unknown")
    number = mapped_column(BigInteger, default=0)
    location: Mapped[str] = mapped_column(String(500), default="Unknown")


class Category_Menu(Base):
    __tablename__ = 'categories_menu'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[int] = mapped_column(primary_key=True)
    bludo: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(300))
    price: Mapped[int] = mapped_column()
    category: Mapped[str] = mapped_column(ForeignKey('categories_menu.id'))
    photo_url: Mapped[str] = mapped_column(String(255))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
