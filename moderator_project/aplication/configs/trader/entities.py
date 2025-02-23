import copy
from attr import dataclass


JSON_MASK = {
    "Version": "2.5",
    "EnableAutoCalculation": 0,
    "EnableAutoDestockAtRestart": 0,
    "EnableDefaultTraderStock": 0,
    "TraderCategories": []
}

JSON_FOOTER = [
    {
        "CategoryName": "---(Денежный-Размен)---",
        "Products": [
            "TraderPlus_Money_Ruble5000,1,-1,1,5000,-1",
            "TraderPlus_Money_Ruble2000,1,-1,1,2000,-1",
            "TraderPlus_Money_Ruble1000,1,-1,1,1000,-1",
            "TraderPlus_Money_Ruble500,1,-1,1,500,-1",
            "TraderPlus_Money_Ruble200,1,-1,1,200,-1",
            "TraderPlus_Money_Ruble100,1,-1,1,100,-1"
        ]
    },
    {
        "CategoryName": "---(Размен-Бабла)---",
        "Products": [
            "TraderPlus_Money_Ruble5000,1,-1,1,5000,-1",
            "TraderPlus_Money_Ruble2000,1,-1,1,2000,-1",
            "TraderPlus_Money_Ruble1000,1,-1,1,1000,-1",
            "TraderPlus_Money_Ruble500,1,-1,1,500,-1",
            "TraderPlus_Money_Ruble200,1,-1,1,200,-1",
            "TraderPlus_Money_Ruble100,1,-1,1,100,-1"
        ]
    }
]
