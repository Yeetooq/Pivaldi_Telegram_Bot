from aiogram import Bot


async def check_sub_channels(bot: Bot, channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if hasattr(chat_member, 'status') and chat_member.status == 'left':
            return False
    return True