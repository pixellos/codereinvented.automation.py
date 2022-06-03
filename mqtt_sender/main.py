import json
import paho.mqtt.client as mqtt

from inverterreader.inverter_reader import ReadItem


def send(address: str, port: int, prefix: str, items: list[ReadItem]):
    client = mqtt.Client()

    try:
        client.connect(address, port, 60)   
        for x in items:
            statePrefix = f"{prefix}/sensor/{x['field']}/state"
            dictionary = {
                "unique_id": x["field"],
                "entity_id": x["field"],
                "id": x["field"],
                "name": x["field"],
                "device_class": "energy",
                "unit_of_measurement": '' if x['unit'] is None else x['unit'],
                "state_topic": statePrefix,
            }
            discoveryPrefix = f"{prefix}/sensor/{x['field']}/config"
            json_object = json.dumps(dictionary, indent=4)
            client.publish(discoveryPrefix, json_object)
            client.publish(statePrefix, x["response"])
    except BaseException as e:
        print("error mqtt", json.dumps(e));
    client.disconnect()
