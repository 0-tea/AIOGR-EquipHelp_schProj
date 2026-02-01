'''Основа'''
import asyncio
from aiogram import Bot, Dispatcher
from typing import Dict, List
from dotenv import load_dotenv
import os
'''Роутеры'''
from commands import router as commands_router
from handlerKB import router as kb_router
from supFuns import wait_router
'''Утилиты'''
from datetime import datetime
from setLogging import logger


bd_bot: Dict[str, List[any]] = {}
"""bot_start_time - время старта программы"""

async def startBot():
    try:
        logger.info("Старт программы..")

        dp = Dispatcher()
        dp.include_router(kb_router)
        dp.include_router(commands_router)
        dp.include_router(wait_router)

        load_dotenv('tokens.env')
        bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))

        await reg_start_time()
        await dp.start_polling(bot, skip_updates=True)

    except Exception:
        logger.critical("Беда с токеном. 🥀")


async def reg_start_time():
    logger.info("Бот запущен 🦺")
    bd_bot['bot_start_time'] = datetime.now()


if __name__ == "__main__":
    asyncio.run(startBot())