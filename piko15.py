import json
import time

import requests

from config import config

DXS = [
    ("dc_voltage_1", 33555202),
    ("dc_ampere_1", 33555201),
    ("dc_power_1", 33555203),

    ("dc_voltage_2", 33555458),
    ("dc_ampere_2", 33555457),
    ("dc_power_2", 33555459),

    ("dc_voltage_3", 33555714),
    ("dc_ampere_3", 33555713),
    ("dc_power_3", 33555715),

    ("output_power", 67109120),
    ("grid_frequency", 67110400),
    ("cos", 67110656),
    ("total_input_dc_power", 33556736),
    ("statistic_day_kwh", 251658754),
    ("statistic_total_kwh", 251658753),
    ("operation_time_hour", 251658496),

    ("ac_voltage_1", 67109378),
    ("ac_ampere_1", 67109377),
    ("ac_power_1", 67109379),

    ("ac_voltage_2", 67109634),
    ("ac_ampere_2", 67109633),
    ("ac_power_2", 67109635),

    ("ac_voltage_3", 67109890),
    ("ac_ampere_3", 67109889),
    ("ac_power_3", 67109891),
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

    def get_results(self, ts=None):
        ts = ts or time.time_ns()
        response = requests.get(self.url).json()
        return [
            dict(value=entry['value'], ts=ts, measurement=DXS_MAPPER[entry['dxsId']])
            for entry in response['dxsEntries']
        ]


if __name__ == '__main__':
    results = Piko15().get_results()
    print(json.dumps(results, indent=2))
