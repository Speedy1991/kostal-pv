import json
import time
import requests
from config import config


DXS = [
    dict(NAME="DC VOLTAGE 1", ID=33555202),
    dict(NAME="DC AMPERE 1", ID=33555201),
    dict(NAME="DC POWER 1", ID=33555203),

    dict(NAME="DC VOLTAGE 2", ID=33555458),
    dict(NAME="DC AMPERE 2", ID=33555457),
    dict(NAME="DC POWER 2", ID=33555459),

    dict(NAME="DC VOLTAGE 3", ID=33555714),
    dict(NAME="DC AMPERE 3", ID=33555713),
    dict(NAME="DC POWER 3", ID=33555715),

    dict(NAME="OUTPUT POWER", ID=67109120),
    dict(NAME="GRID FREQUENCY", ID=67110400),
    dict(NAME="COS", ID=67110656),
    dict(NAME="LIMITATION ON", ID=67110144),

    dict(NAME="AC VOLTAGE 1", ID=67109378),
    dict(NAME="AC AMPERE 1", ID=67109377),
    dict(NAME="AC POWER 1", ID=67109379),

    dict(NAME="AC VOLTAGE 2", ID=67109634),
    dict(NAME="AC AMPERE 2", ID=67109633),
    dict(NAME="AC POWER 2", ID=67109635),

    dict(NAME="AC VOLTAGE 3", ID=67109890),
    dict(NAME="AC AMPERE 3", ID=67109889),
    dict(NAME="AC POWER 3", ID=67109891),
]

DXS_IDS = [v['ID'] for v in DXS]
DXS_MAPPER = {v['ID']: v['NAME'] for v in DXS}


class Piko15:
    tags = dict(
        deviceName='Piko 15',
        deviceType='Inverter'
    )

    def __init__(self):
        url = f"http://{config['PIKO15']['IP']}/api/dxs.json"
        params = "?dxsEntries=" + "&dxsEntries=".join(map(str, DXS_IDS))
        self.url = url + params

    def get_results(self):
        response = requests.get(self.url).json()
        now = time.time_ns()
        return [
            dict(dxsId=entry['dxsId'], name=DXS_MAPPER[entry['dxsId']], value=entry['value'], ts=now)
            for entry in response['dxsEntries']
        ]


if __name__ == '__main__':
    results = Piko15().get_results()
    print(json.dumps(results, indent=2))
