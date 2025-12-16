import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s',
    handlers=[

        logging.StreamHandler()          # Вывод в консоль
    ]
)
logger = logging.getLogger(__name__)

"""

logging.FileHandler('bot.log'),  # Запись в файл
файл удален*

"""