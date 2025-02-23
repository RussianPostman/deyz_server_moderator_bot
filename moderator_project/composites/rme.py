import asyncio
import json
from datetime import datetime
import io
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

async def add_anomaly_return_file(
    message: types.File,
    state: FSMContext,
    bot: Bot,
):
    """
    Хендлер для команды /mode
    """
    config_json = {'s': 123}

    json_str = json.dumps(config_json)

    await message.answer_document(
        types.BufferedInputFile(
            file=json_str.encode('utf-8'),
            filename=f"config_by_{datetime.now().strftime('%Y-%m-%d--%H-%M')}.json"
        )
    )


async def starter(
    token: str,
):
    logging.basicConfig(level=logging.DEBUG)

    bot = Bot(token)
    dp = Dispatcher()

    dp.message.register(add_anomaly_return_file, CommandStart())

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(
            starter(
                '6268111728:AAGePjOYAIW0sYAL06DaLWQ0MV6FaCWBIjo',
            )
        )
    except (KeyboardInterrupt,):
        print('Bot stoped')
