
import time
import requests

def send(ild: str, password: str):
    r = requests.get(
        f'http://dane.pvmonitor.pl/pv/get2.php' + 
        f'?idl={ild}' + 
        f'&p={password}' + 
        f'&tm={time.strftime("%Y-%m-%dT%H:%M:%S")}'  + 
        f'&F2.1=220' + 
        f'&F3.1=11' + 
        f'&F5.1=240' + 
        f'&F6.1=13' 
    )
    r.raise_for_status()

