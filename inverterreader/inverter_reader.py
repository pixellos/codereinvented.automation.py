from logging import error
import time
from typing import TypedDict
from inverterreader.bucketer import Bucket
from pysolarmanv5 import pysolarmanv5


class ReadItem(TypedDict):
    section: str
    field: str
    response: str
    unit: str


def requestForBuckets(
    buckets: list[Bucket], client: pysolarmanv5.PySolarmanV5, verbose=0
):
    result: list[ReadItem] = []
    for bucket in buckets:
        def readBucket(offset: int = 0):
            items = client.read_holding_registers(
                bucket["startAddress"], bucket["length"] + offset
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
                if verbose:
                    print(
                        f'{data["section"]} {data["field"]} {response} {data["unit"]} ',
                        flush=True,
                    )

        try:
            readBucket()
        except BaseException as err:
            error("Error during read: %s %s", bucket, err)
            try: 
                time.sleep(2)
                readBucket(1)
            except BaseException as err:
                error("Error during read retry: %s ", err)

        time.sleep(1)

    return result
