import json
import time
import requests
from config import config


DXS = [
    (dict(ac_dc="dc", type="voltage", phase="1"), 33555202),
    (dict(ac_dc="dc", type="ampere", phase="1"), 33555201),
    (dict(ac_dc="dc", type="power", phase="1"), 33555203),

    (dict(ac_dc="dc", type="voltage", phase="2"), 33555458),
    (dict(ac_dc="dc", type="ampere", phase="2"), 33555457),
    (dict(ac_dc="dc", type="power", phase="2"), 33555459),

    (dict(ac_dc="dc", type="voltage", phase="3"), 33555714),
    (dict(ac_dc="dc", type="ampere", phase="3"), 33555713),
    (dict(ac_dc="dc", type="power", phase="3"), 33555715),

    (dict(name="output", type="power"), 67109120),
    (dict(name="grid frequency"), 67110400),
    (dict(name="cos"), 67110656),
    (dict(name="total input", ac_dc="dc", type="power"), 33556736),
    (dict(name="statistic day", type="kWh"), 251658754),
    (dict(name="statistic total", type="kwh"), 251658753),
    (dict(name="operation time", type="hour"), 251658496),

    (dict(ac_dc="ac", type="voltage", phase="1"), 67109378),
    (dict(ac_dc="ac", type="ampere", phase="1"), 67109377),
    (dict(ac_dc="ac", type="power", phase="1"), 67109379),

    (dict(ac_dc="ac", type="voltage", phase="2"), 67109634),
    (dict(ac_dc="ac", type="ampere", phase="2"), 67109633),
    (dict(ac_dc="ac", type="power", phase="2"), 67109635),

    (dict(ac_dc="ac", type="voltage", phase="3"), 67109890),
    (dict(ac_dc="ac", type="ampere", phase="3"), 67109889),
    (dict(ac_dc="ac", type="power", phase="3"), 67109891),
]

DXS_MAPPER = {v[1]: v[0] for v in DXS}


class Piko15:
    tags = dict(
        deviceName='Piko 15',
        deviceType='Inverter'
    )

    def __init__(self):
        url = f"http://{config['PIKO15']['IP']}/api/dxs.json"
        params = "?dxsEntries=" + "&dxsEntries=".join(map(str, [v[1] for v in DXS]))
        self.url = url + params

    def get_results(self):
        response = requests.get(self.url).json()
        now = time.time_ns()
        return [
            dict(value=entry['value'], ts=now, tags=DXS_MAPPER[entry['dxsId']])
            for entry in response['dxsEntries']
        ]


if __name__ == '__main__':
    results = Piko15().get_results()
    print(json.dumps(results, indent=2))
