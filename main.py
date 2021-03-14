from ksem import KSEM
from piko15 import Piko15
from influx_client import InfluxClient


def create_points(ksem=None, inverter=None):
    points = []
    if ksem:
        for result in ksem.get_results():
            point = InfluxClient.create_idb_point(
                measurement_name=result['name'],
                tags=[(k, v) for k, v in ksem.tags.items()],
                fields=[('value', result['value'])],
                ts=result['ts']
            )
            points.append(point)
    if inverter:
        for result in inverter.get_results():
            point = InfluxClient.create_idb_point(
                measurement_name=result['name'],
                tags=[(k, v) for k, v in inverter.tags.items()],
                fields=[('value', result['value'])],
                ts=result['ts']
            )
            points.append(point)
    return points


def run():
    client = InfluxClient()
    ksem = KSEM()
    inverter = Piko15()

    while True:
        points = create_points(ksem, inverter)
        client.write_points('PV', points)
        print(f"[{len(points)}] Points written to influxdb")


if __name__ == '__main__':
    run()
