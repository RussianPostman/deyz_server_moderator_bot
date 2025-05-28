import base64
import io
import json
from datetime import datetime
from typing import Any

import pandas as pd
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from aiogram import Bot, types

from aiogram.types import BufferedInputFile
from moderator_project.adapters.bot.anomaly.states import AddAnomalyState
from moderator_project.aplication.configs.anomaly.service import AnomalyConfigService


async def add_anomaly_vait_file(
    message: types.Message,
    state: FSMContext,
    bot: Bot,
):
    """
    Хендлер для команды /mode
    """

    await state.clear()
    await state.set_state(AddAnomalyState.vait_file)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Пришлите exel файл конфигурации',
    )


async def add_anomaly_return_file(
    message: types.File,
    state: FSMContext,
    bot: Bot,
    anomaly_ervice: AnomalyConfigService,
):
    """
    Хендлер для команды /mode
    """
    # await state.update_data(name=message.text)
    await state.set_state(AddAnomalyState.return_file)

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    tg_file_path = file.file_path
    file: io.BytesIO = await bot.download_file(tg_file_path)
    file.seek(0)
    df = pd.ExcelFile(file)

    config = anomaly_ervice.create_configs_data(df)
    config_json = json.dumps(config)

    await message.answer_document(
        types.BufferedInputFile(
            file=config_json.encode('utf-8'),
            filename=f"config_by_{datetime.now().strftime('%Y-%m-%d--%H-%M')}.json"
        )
    )

