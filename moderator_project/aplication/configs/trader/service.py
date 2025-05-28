import json
import copy
from collections import defaultdict
from typing import Tuple, Dict, Any

from dataclasses import dataclass

import pandas as pd

from moderator_project.aplication.configs.trader.entities import JSON_FOOTER, JSON_MASK


@dataclass
class PriceParams:
    name: str
    vender: str = None


@dataclass
class TraderPlusServise:

    def read_general_config(self, sheet: pd.ExcelFile):
        buy_config = {}
        sel_config = {}
        wsh = None

        return buy_config, sel_config

    def one_seler_handler(
        salf,
        wsh,
        buy_config: dict,
        sel_config: dict,
        venders_category_list: dict
    ):
        names = wsh.iloc[:, 1]
        value_1 = wsh.iloc[:, 2]
        value_2 = wsh.iloc[:, 3]
        value_3 = wsh.iloc[:, 4]
        buy = wsh.iloc[:, 5]
        sel = wsh.iloc[:, 6]

        data_colls = [names, value_1, value_2, value_3, buy, sel]

        out_list = []
        one_seler_dict = {}
        vender = None

        for row_num in range(len(names)):

            if names[row_num].startswith('('):
                if one_seler_dict.get('CategoryName'):
                    out_list.append(one_seler_dict.copy())
                    one_seler_dict = {}

                venders_category_list[names[row_num].split()[0]].append(names[row_num])
                one_seler_dict['CategoryName'] = names[row_num]
                one_seler_dict['Products'] = []
                vender = names[row_num].strip().split()[0][1:-1].lower()

            else:
                conf_str = ','.join([str(i[row_num]) for i in data_colls[:4]])
                round_by = -1

                # обработка цен на покупку
                if value := buy_config.get((names[row_num], vender)):
                    conf_str += ',' + str(
                        int(round(int(buy[row_num]) * (int(value) / 100), round_by))
                    )

                elif value := buy_config.get((names[row_num], None)):
                    conf_str += ',' + str(
                        int(round(int(buy[row_num]) * (int(value) / 100), round_by))
                    )

                elif value := buy_config.get((one_seler_dict['CategoryName'], vender)):
                    conf_str += ',' + str(
                        int(round(int(buy[row_num]) * (int(value) / 100), round_by))
                    )

                elif value := buy_config.get((one_seler_dict['CategoryName'], None)):
                    conf_str += ',' + str(
                        int(round(int(buy[row_num]) * (int(value) / 100), round_by))
                    )

                else:
                    conf_str += ',' + str(buy[row_num])

                # обработка цен на продажу
                if value := sel_config.get((names[row_num], vender)):
                    conf_str += ',' + str(
                        int(round(int(sel[row_num]) * (int(value) / 100), round_by))
                    )

                elif value := sel_config.get((names[row_num], None)):
                    conf_str += ',' + str(
                        int(round(int(sel[row_num]) * (int(value) / 100), round_by))
                    )

                elif value := sel_config.get((one_seler_dict['CategoryName'], vender)):
                    conf_str += ',' + str(
                        int(round(int(sel[row_num]) * (int(value) / 100), round_by))
                    )

                elif value := sel_config.get((one_seler_dict['CategoryName'], None)):
                    conf_str += ',' + str(
                        int(round(int(sel[row_num]) * (int(value) / 100), round_by))
                    )

                else:
                    conf_str += ',' + str(sel[row_num])

                one_seler_dict['Products'].append(conf_str)

        out_list.append(one_seler_dict.copy())

        return out_list

    def get_full_conf(self, exel_file: pd.ExcelFile):

        buy_config, sel_config = self.read_general_config(exel_file)

        all_items = []
        venders_category_list = defaultdict(list)
        for wsh_name in exel_file.sheet_names[1:]:
            if wsh_name.startswith('+'):
                all_items += self.one_seler_handler(
                    exel_file.parse(wsh_name),
                    buy_config,
                    sel_config,
                    venders_category_list
                )

        prise_result = copy.deepcopy(JSON_MASK)
        prise_result['TraderCategories'] = all_items

        return all_items, venders_category_list