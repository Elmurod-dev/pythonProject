
import asyncio
import logging
import sys
import redis
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from bot.dispacher import TOKEN
from bot.handlers import dp
from bot.middilwares import all_middleware
from db.utils import db
from db.models import *

i18n = I18n(path="locales", default_locale="en", domain="messages")

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # await bot.delete_webhook()
    await all_middleware(dp, i18n)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

