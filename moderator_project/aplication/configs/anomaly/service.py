import copy

import pandas as pd
from pandas import isna

from moderator_project.aplication.configs.anomaly.entities import MASTER_TEMPLATE, FullAnomaly, SETTINGS_DICT, \
    ArtefactsSettings, JSON_TEMPLATE, ARTEFACT_TEMPLATE
from moderator_project.aplication.configs.anomaly.enums import Columns


class AnomalyConfigService:

    def _read_defoult_settings(self, anomaly: FullAnomaly, wsh) -> None:
        settings_dict = {}

        for _, row in wsh.iterrows():
            if (
                    isinstance(row.iloc[Columns.SETTINGS_KEY.value], str)
                    and not isna(row.iloc[Columns.SETTINGS_VALUE.value])
            ):
                settings_dict[Columns.SETTINGS_KEY.value] = (
                    Columns.SETTINGS_VALUE.value
                )

        for set_key, set_value in settings_dict.items():
            anomaly.__setattr__(SETTINGS_DICT[set_key.strip()], set_value)

    def _read_coordinates(self, wsh) -> list[list[float]]:
        """

        """
        out_list = []
        for _, row in wsh.iterrows():
            if (
                isinstance(row.iloc[Columns.COORDINATE.value], str)
                and not isna(row.iloc[Columns.COORDINATE.value])
            ):
                out_list.append(
                    [
                        float(num.strip())
                        for num in row.iloc[Columns.COORDINATE.value].split(',')
                    ]
                )

        return out_list

    def _read_detectors(self, wsh) -> list[str]:
        """

        """
        out_list = []
        for _, row in wsh.iterrows():
            if (
                isinstance(row.iloc[Columns.DETEKTOR.value], str)
                and not isna(row.iloc[Columns.DETEKTOR.value])
            ):

                out_list.append(row.iloc[Columns.DETEKTOR.value])

        return out_list

    def _read_artefacts(self, wsh, ofset: int) -> list[ArtefactsSettings]:
        artefacts_list = []

        for _, row in wsh.iterrows():
            if isna(row.iloc[ofset]):
                break

            art_name = row.iloc[ofset]
            art_chanse = row.iloc[ofset + 1]
            artefacts_list.append(
                ArtefactsSettings(
                    Classname=art_name,
                    Chance=art_chanse,
                )
            )
        return artefacts_list

    def _get_one_anomaly(self, list_name: str, exel_file: pd.ExcelFile) -> FullAnomaly:
        """
        Собирает данные по одной аномалии
        """
        wsh = exel_file.parse(list_name)

        anomaly_classname = list_name.split('_')[0]
        anomaly_obj = FullAnomaly(
            classname=anomaly_classname,
            full_name=list_name,
            anomaly_template=copy.deepcopy(JSON_TEMPLATE),
            artefact_template=copy.deepcopy(ARTEFACT_TEMPLATE),
        )
        anomaly_obj.positions = self._read_coordinates(wsh)

        # счётчик колонок, на случай переменного количества детекторов
        column_number = Columns.ARTEFACT.value
        list_of_detectors = self._read_detectors(wsh)
        artefacts_mapp = {}

        for detector in list_of_detectors:
            art_settings = self._read_artefacts(wsh, column_number)
            artefacts_mapp[detector] = art_settings
            column_number += 2

        anomaly_obj.artefacts_mapp = artefacts_mapp

        return anomaly_obj


    def create_configs_data(self, exel_file: pd.ExcelFile) -> list[FullAnomaly]:
        """
        Создаёт полный набор данных под конфиг файл аномалий
        """
        anomalies = []

        for list_name in exel_file.sheet_names:
            anomalies.append(
                self._get_one_anomaly(list_name, exel_file)
            )

        temlate = copy.deepcopy(MASTER_TEMPLATE)

        temlate['AnomalyList'] = [
            anomaly.convert_to_json() for anomaly in anomalies
        ]

        return temlate
