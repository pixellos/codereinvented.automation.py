import json
import paho.mqtt.client as mqtt

from inverterreader.inverter_reader import ReadItem


def send(address: str, port: int, prefix: str, items: list[ReadItem]):
    client = mqtt.Client()
    client.connect(address, port, 60)

    for x in items:
        statePrefix = f"{prefix}/sensor/{x['field']}/state"
        dictionary = {
            "id": x["field"],
            "name": x["field"],
            "device_class": "energy",
            "state_topic": statePrefix,
        }
        discoveryPrefix = f"{prefix}/sensor/{x['field']}/config"

        json_object = json.dumps(dictionary, indent=4)
        client.publish(discoveryPrefix, json_object)
        client.publish(statePrefix, x["response"])

    client.disconnect()
