from logging import error
import time
from typing import TypedDict
import requests

from common.json import JsonHelper
from inverterreader.inverter_reader import ReadItem


class Entry(TypedDict):
    id: str
    description: str
    unit: str


class Mapping(TypedDict):
    pvMonitorId: int
    section: str
    fieldId: str


idMapsHelper = JsonHelper[Entry]("pvmonitor_sender/idmap.json")
sofarMapHelper = JsonHelper[Mapping]("pvmonitor_sender/sofar_hyd_g9_map.json")


def send(ild: str, password: str, inverterId: int, items: list[ReadItem]):
    sofarMap = sofarMapHelper.readFromFile()

    query = ""
    idsToReadItems = dict(zip(map(lambda x: (x["section"], x["field"]), items), items))

    for x in sofarMap:
        key = (x["section"], x["fieldId"])
        try:
            item = idsToReadItems[key]
            query += f'&F{x["pvMonitorId"]}.{inverterId}={item["response"]}'
        except:
            error("Cannot match entries %s", item)

    r = requests.get(
        f"http://dane.pvmonitor.pl/pv/get2.php"
        + f"?idl={ild}"
        + f"&p={password}"
        + f'&tm={time.strftime("%Y-%m-%dT%H:%M:%S")}'
        + query
    )
    r.raise_for_status()
