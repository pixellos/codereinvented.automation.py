from json import load, dump
from genericpath import exists
from typing import Generic, TypeVar


T = TypeVar('T')    

class JsonHelper(Generic[T]):
    def __init__(self, fileName: str):
        self.fileName = fileName    

    def dumpJson(self, data: list[T]):
        with open(self.fileName, "w") as f:
            dump(data, f, ensure_ascii=False, indent=2)

    def readFromFile(self)-> list[T]:
        with open(self.fileName, "r") as f:
            return load(f)

    def cacheExists(self):
        return exists(self.fileName)