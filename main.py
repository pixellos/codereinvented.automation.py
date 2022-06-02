import logging
import time
from typing import TypedDict
from time import sleep
from pysolarmanv5 import pysolarmanv5
from common.json import JsonHelper
from inverterreader.bucketer import Bucket, bucketIdentifiers
from inverterreader.inverter_reader import ReadItem, requestForBuckets
from pvmonitor_sender.main import send
from mqtt_sender.main import send as send_mqtt
from xlsxparser.sofar_modbus_protocol import (
    jsonHelper,
    dumpToCache,
)
import os


if __name__ == "__main__":
    logging.basicConfig(
        filename="logger.log",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    loggerIp = os.environ["logger__ip"]
    loggerPort = int(os.environ["logger__port"])
    loggerSerial = int(os.environ["logger__serial"])
    inverterSlaveId = int(os.environ["inverter__slaveid"])

    pvMonitorLogin = os.environ.get("pvmonitor__login", None)
    pvMonitorPassword = os.environ.get("pvmonitor__password", None)
    pvMonitorNumber = os.environ.get("pvmonitor__lp", None)

    mqttAddress = os.environ.get("mqtt__address", "mosquitto")
    mqttPort = os.environ.get("mqtt__port", 1883)
    mqttPrefix = os.environ.get("mqtt__prefix", "homeassistant")

    verbose = int(os.environ["verbose"])

    def execute():
        client = pysolarmanv5.PySolarmanV5(
            address=loggerIp,
            serial=loggerSerial,
            port=loggerPort,
            slave_id=inverterSlaveId,
            verbose=verbose,
        )
        entries = (
            dumpToCache() if not jsonHelper.cacheExists() else jsonHelper.readFromFile()
        )
        buckets = bucketIdentifiers(entries)
        result = requestForBuckets(buckets, client, verbose)

        responseJsonHelper = JsonHelper[ReadItem](
            f'results/resp-{time.strftime("%Y%m%d-%H%M%S")}.json'
        )
        responseJsonHelper.dumpJson(result)
        return result

    lastPvMonitorTime = time.time()
    while True:
        result = execute()

        if time.time() - lastPvMonitorTime > 300:
            lastPvMonitorTime = time.time()
            if pvMonitorLogin and pvMonitorPassword and pvMonitorNumber:
                send(pvMonitorLogin, pvMonitorPassword, int(pvMonitorNumber), result)

        if mqttAddress and mqttPort and mqttPrefix and result:
            send_mqtt(mqttAddress, mqttPort, mqttPrefix, result)
