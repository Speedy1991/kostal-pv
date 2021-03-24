import time

from ksem import KSEM
from piko15 import Piko15
from influx_client import InfluxClient


def create_points(instance, ts=None):
    points = []
    meta_tags = instance.tags
    for result in instance.get_results(ts):
        fields = dict(value=result['value'])
        point = InfluxClient.create_idb_point(
            measurement_name=result['measurement'],
            tags=meta_tags,
            fields=fields,
            ts=result['ts']
        )
        points.append(point)
    return points


def run():
    client = InfluxClient()
    ksem = KSEM()
    inverter = Piko15()

    while True:
        ts = time.time_ns()
        points = [*create_points(ksem, ts), *create_points(inverter, ts)]
        if len(points) > 0:
            client.write_points('PV New', points)
            print(f"[{len(points)}] Points written to influxdb")


if __name__ == '__main__':
    run()
