import copy
from enum import Enum
from dataclasses import dataclass


class Columns(Enum):
    COORDINATE = 0
    DETEKTOR = 1
    SETTINGS_KEY = 2
    SETTINGS_VALUE = 3
    ARTEFACT = 4


class BoolChoose(Enum):
    TRUE = 1
    FALSE = 0


class SettingsDefoult(Enum):
    def_chanse = 100
    def_max_arts = 1
