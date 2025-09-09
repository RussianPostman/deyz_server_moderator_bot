import base64
import io
import json
from datetime import datetime

import pandas as pd
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from aiogram import Bot, types
from aiogram.types import BufferedInputFile

from moderator_project.adapters.bot.trader_plus.states import AddTraderState
from moderator_project.aplication.configs.trader.service import TraderPlusServise


async def add_trader_vait_file(
    message: types.Message,
    state: FSMContext,
    bot: Bot,
):
    """
    Начало добавления нового конфига трейдер+
    """

    await state.clear()
    await state.set_state(AddTraderState.vait_file)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=(
            'Конфигуратор трейдер+\n'
            'Пришлите exel файл конфигурации'
        ),
    )


async def add_trader_return_file(
    message: types.File,
    state: FSMContext,
    bot: Bot,
    trader_ervice: TraderPlusServise,
):
    """
    ...
    """

    await state.set_state(AddTraderState.return_file)

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    tg_file_path = file.file_path
    file: io.BytesIO = await bot.download_file(tg_file_path)
    file.seek(0)
    df = pd.ExcelFile(file)

    all_items, venders_category_list = trader_ervice.get_full_conf(df)

    config_json = json.dumps(all_items, ensure_ascii=False, indent=4)
    venders_category_json = json.dumps(
        venders_category_list,
        ensure_ascii=False,
        indent=4,
    )
    date = datetime.now().strftime('%Y-%m-%d--%H-%M')

    await message.answer_document(
        types.BufferedInputFile(
            file=config_json.encode('utf-8'),
            filename=f"venders_config_by_{date}.json"
        )
    )
    await message.answer_document(
        types.BufferedInputFile(
            file=venders_category_json.encode('utf-8'),
            filename=f"venders_category_config_by_{date}.json"
        )
    )

