import time
from typing import TypedDict
from xlsxparser.sofar_modbus_protocol import Identifier
from pysolarmanv5 import pysolarmanv5


class Bucket(TypedDict):
    startAddress: int
    length: int
    items: list[Identifier]


def bucket(xs: list[Identifier], size: int):
    if not any(xs):
        return []

    xs = xs.copy()
    result: list[Bucket] = []
    while any(xs):
        current = [xs.pop()]
        first = current[0]
        if any(xs):
            element = xs[-1]
            if element["address"] - first["address"] < size:
                element = xs.pop()
                while (element["address"] - first["address"]) < size and any(xs):
                    current.append(element)
                    if any(xs):
                        element = xs.pop()

        result.append(
            {
                "items": current,
                "length": current[-1]["address"] - first["address"] + 1,
                "startAddress": first["address"],
            }
        )
    return result


def addressPresent(x: Identifier) -> bool:
    return x["address"] is not None


def bucketIdentifiers(entries: list[Identifier]):
    result = list(filter(addressPresent, entries))
    result.reverse()
    return bucket(result, 50)
