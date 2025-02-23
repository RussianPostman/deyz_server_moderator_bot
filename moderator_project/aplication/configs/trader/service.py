import json
import time
from typing import Tuple, Dict, Any

import gspread
from pprint import pprint
from dataclasses import dataclass

import pandas as pd

from moderator_project.aplication.configs.trader.entities import JSON_FOOTER, JSON_MASK


@dataclass
class PriceParams:
    name: str
    vender: str = None


class AnomalyConfigService:

    @staticmethod
    def _read_config(exel_file: pd.ExcelFile) -> tuple[dict[Any, Any | None], Any]:
        buy_config = {}
        sel_config = {}
        wsh = None

        for list_name in exel_file.sheet_names():
            if list_name == 'Конфиг +':
                wsh = exel_file.parse(list_name)

        if not wsh:
            return {}, {}

        names = wsh.col_values(2)[1:]

        # задаются генераторы для удобного перебора значений
        buy_names = (i for i in names)
        buy_price = (i for i in wsh.col_values(3)[1:])
        buy_is_active = (i for i in wsh.col_values(4)[1:])
        buy_vender = (i for i in wsh.col_values(5)[1:])

        sel_names = (i for i in names)
        sel_price = (i for i in wsh.col_values(6)[1:])
        sel_is_active = (i for i in wsh.col_values(7)[1:])
        sel_vender = (i for i in wsh.col_values(8)[1:])

        for price in buy_price:
            name = next(buy_names).strip()
            active = next(buy_is_active).strip()
            vender = next(buy_vender).strip()
            vender = vender.lower() if len(vender) >= 2 else None

            if len(price.strip()) > 0 and 'да' in active.lower():
                buy_config[(name, vender)] = price

        for price in sel_price:
            name = next(sel_names).strip()
            active = next(sel_is_active).strip()
            vender = next(sel_vender).strip().lower()
            vender = vender.lower() if len(vender) >= 2 else None

            if len(price.strip()) > 0 and 'да' in active.lower():
                sel_config[(name, vender)] = price

        return buy_config, sel_config

    @staticmethod
    def _one_seler_handler(
            wsh: gspread.Worksheet,
            buy_config: dict,
            sel_config: dict,
            venders_category_list: list
    ):
        """
        Обработчик таблицы одного вендора
        """
        names = wsh.col_values(2)
        value_1 = wsh.col_values(3)
        value_2 = wsh.col_values(4)
        value_3 = wsh.col_values(5)
        buy = wsh.col_values(6)
        sel = wsh.col_values(7)

        data_colls = [names, value_1, value_2, value_3, buy, sel]

        out_list = []
        one_seler_dict = {}
        vender = None

        for row_num in range(1, len(names)):

            if names[row_num].startswith('('):
                if one_seler_dict.get('CategoryName'):
                    out_list.append(one_seler_dict.copy())
                    one_seler_dict = {}

                venders_category_list.append(names[row_num])
                one_seler_dict['CategoryName'] = names[row_num]
                one_seler_dict['Products'] = []
                vender = names[row_num].strip().split()[0][1:-1].lower()

            elif value_1[row_num] and value_1[row_num][-1].isdigit():
                conf_str = ','.join([str(i[row_num]) for i in data_colls[:4]])
                round_by = -1

                # обработка цен на покупку
                buy_int = int(buy[row_num])


                if value := buy_config.get((names[row_num], vender)):
                    conf_str += ',' + str(
                        int(round(buy_int * (int(value) / 100), round_by))
                    )

                elif value := buy_config.get((names[row_num], None)):
                    conf_str += ',' + str(
                        int(round(buy_int * (int(value) / 100), round_by))
                    )

                elif value := buy_config.get((one_seler_dict['CategoryName'], vender)):
                    conf_str += ',' + str(
                        int(round(buy_int * (int(value) / 100), round_by))
                    )

                elif value := buy_config.get((one_seler_dict['CategoryName'], None)):
                    conf_str += ',' + str(
                        int(round(buy_int * (int(value) / 100), round_by))
                    )

                else:
                    conf_str += ',' + str(buy[row_num])

                # обработка цен на продажу
                sel_int = int(sel[row_num])

                if value := sel_config.get((names[row_num], vender)):
                    conf_str += ',' + str(
                        int(round(sel_int * (int(value) / 100), round_by))
                    )

                elif value := sel_config.get((names[row_num], None)):
                    conf_str += ',' + str(
                        int(round(sel_int * (int(value) / 100), round_by))
                    )

                elif value := sel_config.get((one_seler_dict['CategoryName'], vender)):
                    conf_str += ',' + str(
                        int(round(sel_int * (int(value) / 100), round_by))
                    )

                elif value := sel_config.get((one_seler_dict['CategoryName'], None)):
                    conf_str += ',' + str(
                        int(round(sel_int * (int(value) / 100), round_by))
                    )

                else:
                    conf_str += ',' + str(sel[row_num])

                one_seler_dict['Products'].append(conf_str)

        out_list.append(one_seler_dict.copy())

        return out_list

    def create_trader_config(self, exel_file: pd.ExcelFile):
        """
        Создать конфиг для TraderPlus 2.5
        """

        buy_config, sel_config = self._read_config(exel_file)

        all_items = []
        venders_category_list = []
        for list_name in exel_file.sheet_names():
            if list_name.startswith('+'):
                all_items += self._one_seler_handler(
                    exel_file.parse(list_name),
                    buy_config,
                    sel_config,
                    venders_category_list
                )

        all_items += JSON_FOOTER
        JSON_MASK['TraderCategories'] = all_items

        return JSON_MASK, venders_category_list
