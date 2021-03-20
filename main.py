from ksem import KSEM
from piko15 import Piko15
from influx_client import InfluxClient


def create_points(instance):
    points = []
    meta_tags = instance.tags
    for result in instance.get_results():
        point_tags = result['tags']
        point_tags.update(meta_tags)
        fields = dict(value=result['value'])
        fields.update({
            '_'.join(point_tags.values()): result['value']
        })
        point = InfluxClient.create_idb_point(
            measurement_name=result.get('name', None),
            tags=point_tags,
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
        points = [*create_points(ksem), *create_points(inverter)]
        if len(points) > 0:
            client.write_points('PV', points)
            print(f"[{len(points)}] Points written to influxdb")


if __name__ == '__main__':
    run()
