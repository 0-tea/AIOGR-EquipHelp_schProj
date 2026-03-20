'''Основа'''
import asyncio
from aiogram import Bot, Dispatcher
from typing import Dict, List
from dotenv import load_dotenv
import os
import json
'''Роутеры'''
from commands import router as commands_router
from handlerKB import router as kb_router
from supFuns import wait_router_sup
from neuroChatting import wait_router_Ai
from rooms import wait_router_rooms
'''Утилиты'''
from aiogram.client.session.aiohttp import AiohttpSession
from datetime import datetime
from setLogging import logger

load_dotenv('tokens.env')
PROXY_URL = os.getenv("PROXY_URL")
session = AiohttpSession(
    proxy=PROXY_URL,
    json_loads=json.loads,
    json_dumps=json.dumps
)

bd_bot: Dict[str, List[any]] = {}
"""bot_start_time - время старта программы"""
async def startBot():
    try:
        logger.info("Старт программы..")

        dp = Dispatcher()
        dp.include_router(kb_router)
        dp.include_router(commands_router)
        dp.include_router(wait_router_sup)
        dp.include_router(wait_router_Ai)
        dp.include_router(wait_router_rooms)

        bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'), session=session)

        await reg_start_time()
        await dp.start_polling(bot, skip_updates=True)


    except Exception as e:
        logger.critical("Беда с токеном. 🥀", e)


async def reg_start_time():
    logger.info("Бот запущен 🦺")
    bd_bot['bot_start_time'] = datetime.now()


if __name__ == "__main__":
    asyncio.run(startBot())