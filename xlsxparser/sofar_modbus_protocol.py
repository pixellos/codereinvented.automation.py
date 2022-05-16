from fileinput import filename
from genericpath import exists
from textwrap import indent
from json import load,  dump
from typing import TypedDict
import openpyxl
from pathlib import Path

defaultFileName = "data.json"

class Identifier(TypedDict):
    section: str
    address: str
    field: str
    type: str
    accuracy: str
    unit: str
    description: str
    mask: str
    mask2: str

def readFromXlsx(startRow: int, endRow: int, sectionName: str):
    file = Path("SOFAR HYD-3PH and SOFAR -G3 Modbus Protocol 2021-10-14_Client.xlsx")
    wb = openpyxl.load_workbook(file, read_only=True)
    registers = wb["Registers"]
    result: list[Identifier] = []
    for row in registers.iter_rows(startRow, endRow):
        result.append(
            {
                "section": sectionName,
                "address": int(str(row[1].value), 16) if row[1].value is not None else None,
                "field": row[2].value,
                "type": row[3].value,
                "accuracy": row[4].value,
                "unit": row[5].value,
                "description": row[9].value,
                "mask": row[11].value,
                "mask2": row[12].value,
            }
        )
    return result

def readFromFile(fileName:str = defaultFileName)-> list[Identifier]:
    with open(fileName, "r") as f:
        return load(f)

def cacheExists(fileName: str = defaultFileName):
    return exists(fileName)

def dumpToCache(fileName: str = defaultFileName): 
    result = (
        readFromXlsx(135, 205, "On-Grid")
        + readFromXlsx(207, 272, "Off-Grid")
        + readFromXlsx(274, 392, "PV")
        + readFromXlsx(394, 492, "Battery")
        + readFromXlsx(494, 558, "Power")
    )

    def onlyWithField(x: Identifier) -> bool:
        return x["field"] is not None and x['type'] is not None

    data = list(filter(onlyWithField, result))
    dumpJson(data, fileName); 
    return result

def dumpJson(data: any, fileName: str):
    with open(fileName, "w") as f:
        dump(data, f, ensure_ascii=False, indent=2)

