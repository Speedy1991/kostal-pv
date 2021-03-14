import json
import time

import requests

DXS = [
    dict(NAME="DC_VOLTAGE_1", ID=33555202),
    dict(NAME="DC_AMPERE_1", ID=33555201),
    dict(NAME="DC_POWER_1", ID=33555203),

    dict(NAME="DC_VOLTAGE_2", ID=33555458),
    dict(NAME="DC_AMPERE_2", ID=33555457),
    dict(NAME="DC_POWER_2", ID=33555459),

    dict(NAME="DC_VOLTAGE_3", ID=33555714),
    dict(NAME="DC_AMPERE_3", ID=33555713),
    dict(NAME="DC_POWER_3", ID=33555715),

    dict(NAME="OUTPUT_POWER", ID=67109120),
    dict(NAME="GRID_FREQUENCY", ID=67110400),
    dict(NAME="COS", ID=67110656),
    dict(NAME="LIMITATION_ON", ID=67110144),

    dict(NAME="AC_VOLTAGE_1", ID=67109378),
    dict(NAME="AC_AMPERE_1", ID=67109377),
    dict(NAME="AC_POWER_1", ID=67109379),

    dict(NAME="AC_VOLTAGE_2", ID=67109634),
    dict(NAME="AC_AMPERE_2", ID=67109633),
    dict(NAME="AC_POWER_2", ID=67109635),

    dict(NAME="AC_VOLTAGE_3", ID=67109890),
    dict(NAME="AC_AMPERE_3", ID=67109889),
    dict(NAME="AC_POWER_3", ID=67109891),
]

DXS_IDS = [v['ID'] for v in DXS]
DXS_MAPPER = {v['ID']: v['NAME'] for v in DXS}


IP = "192.168.178.100"

if __name__ == '__main__':
    url = f"http://{IP}/api/dxs.json"
    params = "?dxsEntries=" + "&dxsEntries=".join(map(str, DXS_IDS))
    url = url + params
    response = requests.get(url).json()

    now = time.time()
    result = [
        dict(dxsId=entry['dxsId'], name=DXS_MAPPER[entry['dxsId']], value=entry['value'], ts=now)
        for entry in response['dxsEntries']
    ]
    result = json.dumps(result, indent=2)
    print(result)
