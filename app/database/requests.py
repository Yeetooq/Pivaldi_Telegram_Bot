from sqlalchemy import select, and_

from app.database.models import async_session
from app.database.models import User, Category_Menu, Menu


async def set_user(tg_id: int, tg_username: str, name: str = "Unknown") -> None:
    async with async_session() as session:
        user = User(tg_id=tg_id, tg_username=tg_username, name=name)
        session.add(user)
        await session.commit()



async def set_reg(tg_id: int, name: str, number: int, location: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            if name:
                user.name = name
            if number:
                user.number = number
            if location:
                user.location = location

            await session.commit()


async def delete_info(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == tg_id))
        user = user.scalar_one_or_none()

        if user:
            user.name = None
            user.number = None
            user.location = None

            await session.commit()


async def update_user_stats(tg_id: int, win: bool) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            if win:
                user.win += 1
            else:
                user.lose += 1

            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category_Menu))


async def get_category_menu(category_id):
    async with async_session() as session:
        return await session.scalars(select(Menu).where(Menu.category == category_id))


async def get_menu(menu_id):
    async with async_session() as session:
        return await session.scalar(select(Menu).where(Menu.id == menu_id))


async def get_lyudi():
    async with async_session() as session:
        return await session.scalars(select(User.tg_id))


async def get_user_win(tg_id: int) -> int:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            return user.win
        else:
            return 0  # Если пользователь не найден, возвращаем 0


async def get_user_lose(tg_id: int) -> int:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            return user.lose
        else:
            return 0  # Если пользователь не найден, возвращаем 0


async def calculate_win_percentage(tg_id: int) -> float:
    wins = await get_user_win(tg_id)
    loses = await get_user_lose(tg_id)
    total_games = wins+loses
    if total_games == 0:
        return 0.0  # Если у пользователя нет игр, вернуть 0 процентов

    win_percentage = (wins / total_games) * 100
    return round(win_percentage, 2)  # Округляем до двух знаков после запятой
