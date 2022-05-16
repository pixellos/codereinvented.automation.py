import time
from typing import TypedDict
from pysolarmanv5 import pysolarmanv5
import requests
from inverterreader.bucketer import bucketIdentifiers
from xlsxparser.sofar_modbus_protocol import (
    Identifier,
    cacheExists,
    dump,
    dumpJson,
    dumpToCache,
    readFromFile,
)
import os

modbusFileCache = "cache/sofar_hyd_3ph_g3.json"
entries = dumpToCache(modbusFileCache) if not cacheExists(modbusFileCache) else readFromFile(modbusFileCache)
buckets = bucketIdentifiers(entries)

loggerIp = os.environ["logger__ip"]
loggerPort = int(os.environ["logger__port"])
loggerSerial = int(os.environ["logger__serial"])
inverterSlaveId = int(os.environ["inverter__slaveid"])
verbose = int(os.environ["verbose"])

client = pysolarmanv5.PySolarmanV5(
    address=loggerIp,
    serial=loggerSerial,
    port=loggerPort,
    slave_id=inverterSlaveId,
    verbose=verbose,
)

class ReadItem(TypedDict):
    section: str
    field: str
    response: str
    unit: str


result: list[ReadItem] = []


while True:
    for bucket in buckets:
        time.sleep(0.2)
        try:
            items = client.read_holding_registers(
                bucket["startAddress"], bucket["length"]
            )
            for data in bucket["items"]:
                position = data["address"] - bucket["startAddress"]
                isSigned = 1 if data["type"] and data["type"][0] == "I" else 0
                length = int(int(data["type"][1:]) / 16)
                scale = 1 if data["accuracy"] is None else data["accuracy"]
                response = client._format_response(
                    items[position : position + length], signed=isSigned, scale=scale
                )
                result.append(
                    {
                        "field": data["field"],
                        "response": response,
                        "section": data["section"],
                        "unit": data["unit"],
                    }
                )
                print(
                    f'{data["section"]} {data["field"]} {response} {data["unit"]} ',
                    flush=True,
                )
        except:
            None

    dumpJson(result, f'results/resp-{time.strftime("%Y%m%d-%H%M%S")}.json')
    time.sleep(20)
