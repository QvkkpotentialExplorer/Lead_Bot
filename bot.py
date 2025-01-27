import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from yookassa import Configuration

from config import load_config
from tg_bot.tg_bott.handlers import start
from tg_bot.tg_bott.scripts import send_thanks_message

# redis_url = config('REDIS_URL')

logger = logging.getLogger(__name__)


def register_filters(dp):
    pass


def register_handler(dp):
    """
    Функция для регистрации твоего хендлера.Создаешь в папочке handlers file и прописываешь нужные тебе хендлеры,
    далее делаешь функцию register {{group_handlers_name}} и по очереди регаешь их в функции register, потом импортируешь её сюда
    :param dp:
    :return:
    """
    # register_start(dp)

    # register_echo(dp)
    # register_ongoing(dp)


async def main():

    # async with db_helper.session_factory() as session:
    #     await create_default_db(session=session)

    # await db.create_table()

    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    config = load_config(path=r'.env')
    bot = Bot(token=config.tg_bot.token)
    # storage = RedisStorage.from_url(config('REDIS_URL'))
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)

    dp.include_routers(start.router)
    register_filters(dp)
    register_handler(dp)
    #
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_thanks_message, 'interval', seconds = 10, args=(bot,))
    try:
        scheduler.start()
        await dp.start_polling(bot)

    finally:
        await dp.storage.close()

        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main=main())
    except(KeyboardInterrupt, SystemExit, RuntimeError):
        logger.error('Все кончается')
