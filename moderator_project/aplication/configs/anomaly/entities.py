import copy
from attr import dataclass

from moderator_project.aplication.configs.anomaly.enums import BoolChoose


@dataclass
class ArtefactsSettings:
    Classname: str
    Chance: int


@dataclass
class FullAnomaly:
    classname: str
    full_name: str
    positions: list[float] = None
    artefacts_mapp: dict = None

    Chance_To_Spawn: int = 100
    Enable_Spawn_ArtefactsWithDetectors: BoolChoose = BoolChoose.TRUE.value
    MaxInOnePoint: int = 1

    anomaly_template: dict = None
    artefact_template: dict[str, list[ArtefactsSettings]] = None

    def convert_to_json(self):
        template = self.anomaly_template

        template['Unique_Group_Title'] = self.full_name
        template['Classname_Anomaly_Object'] = self.classname
        template['Positions_Spawn_Anomaly'] = self.positions
        template['Chance_To_Spawn'] = self.Chance_To_Spawn
        template['Enable_Spawn_ArtefactsWithDetectors'] = self.Enable_Spawn_ArtefactsWithDetectors
        template['MaxInOnePoint'] = self.MaxInOnePoint
        template['ArtefactsWithDetectors']['MaxInOnePoint'] = self.MaxInOnePoint

        for detector, art_settings in self.artefacts_mapp.items():
            artefact_settings = copy.deepcopy(self.artefact_template)

            artefact_settings['Classname_Detector'] = detector
            artefact_settings['Detect_Artefacts_Settings'] = [
                art.__dict__ for art in art_settings
            ]
            template['ArtefactsWithDetectors']['ArtefactsList'].append(artefact_settings)

        return template


SETTINGS_DICT = {
    'Шанс на спавн': 'Chance_To_Spawn',
    'Включить артефакты': 'Enable_Spawn_ArtefactsWithDetectors',
    'Макс артефактов': 'MaxInOnePoint'
}

JSON_TEMPLATE = {
    "Unique_Group_Title": "...",  #
    "Classname_Anomaly_Object": "...",  #
    "Chance_To_Spawn": 100,
    "Positions_Spawn_Anomaly": [],  #
    "Enable_Spawn_ArtefactsWithoutDetectors": 0,
    "Enable_Spawn_ArtefactsWithDetectors": 1,
    "ArtefactsWithoutDetectors": {
        "MaxInOnePoint": 0,
        "ArtefactsList": []
    },
    "ArtefactsWithDetectors": {
        "MaxInOnePoint": 1,  #
        "ArtefactsList": []  #
    }
}
ARTEFACT_TEMPLATE = {
    "Classname_Detector": "...",   #
    "Detect_Artefacts_Settings": []   #
}


MASTER_TEMPLATE = {
    "DebugLogs_enabled": 0,
    "DetectorsConfig": [
        {
            "ClassName": "Anomaly_Detector_Otklik",
            "Radius": 10.0
        },
        {
            "ClassName": "Anomaly_Detector_Medved",
            "Radius": 15.0
        },
        {
            "ClassName": "Anomaly_Detector_Svarog",
            "Radius": 20.0
        }
    ],
    "AnomalyList": [],
	"Teleports" : []
}
