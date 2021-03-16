from ksem import KSEM
from piko15 import Piko15
from influx_client import InfluxClient
import time


def create_points(instance):
    points = []
    for result in instance.get_results():
        meta_tags = [(k, v) for k, v in instance.tags.items()]
        point_tags = [(k, v) for k, v in result['tags'].items()]
        point = InfluxClient.create_idb_point(
            measurement_name=result['name'],
            tags=[*meta_tags, *point_tags],
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
        try:
            points = [*create_points(ksem), *create_points(inverter)]
            client.write_points('PV', points)
            print(f"[{len(points)}] Points written to influxdb")
        except Exception as e:
            print(e)
            time.sleep(10)


if __name__ == '__main__':
    run()
