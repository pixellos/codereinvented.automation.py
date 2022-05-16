import time
from typing import TypedDict
from time import sleep
from pysolarmanv5 import pysolarmanv5
from common.json import JsonHelper
from inverterreader.bucketer import Bucket, bucketIdentifiers
from inverterreader.inverter_reader import ReadItem, requestForBuckets
from pvmonitor_sender.main import send
from xlsxparser.sofar_modbus_protocol import (
    jsonHelper,
    dumpToCache,
)
import os


if __name__ == "__main__":
    loggerIp = os.environ["logger__ip"]
    loggerPort = int(os.environ["logger__port"])
    loggerSerial = int(os.environ["logger__serial"])
    inverterSlaveId = int(os.environ["inverter__slaveid"])

    pvMonitorLogin = os.environ.get("pvmonitor__login", None)
    pvMonitorPassword = os.environ.get("pvmonitor__password", None)
    pvMonitorNumber = os.environ.get("pvmonitor__lp", None)

    verbose = int(os.environ["verbose"])

    client = pysolarmanv5.PySolarmanV5(
        address=loggerIp,
        serial=loggerSerial,
        port=loggerPort,
        slave_id=inverterSlaveId,
        verbose=verbose,
    )

    def execute():
        entries = (
            dumpToCache() if not jsonHelper.cacheExists() else jsonHelper.readFromFile()
        )
        buckets = bucketIdentifiers(entries)
        result = requestForBuckets(buckets, client, verbose)

        if pvMonitorLogin and pvMonitorPassword and pvMonitorNumber:
            send(pvMonitorLogin, pvMonitorPassword, int(pvMonitorNumber), result)

        responseJsonHelper = JsonHelper[ReadItem](
            f'results/resp-{time.strftime("%Y%m%d-%H%M%S")}.json'
        )
        responseJsonHelper.dumpJson(result)

    while True:
        execute()
        sleep(240)
