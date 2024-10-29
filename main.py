import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from constants import SHORT_DESCRIPTION, DESCRIPTION
from user_private.handlers import user_router
from common.commands import private
import config


config = config.Config()

bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

dp.include_routers(user_router)


async def on_startup():
    pass


async def on_shutdown():
    pass


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_short_description(SHORT_DESCRIPTION)
    await bot.set_my_description(DESCRIPTION)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info('Бот включен')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
