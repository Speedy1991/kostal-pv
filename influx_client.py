import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
from config import config
from influxdb_client.domain.write_precision import WritePrecision


class InfluxClient:
    def __init__(self):
        self.client = InfluxDBClient(
            url=config['INFLUX']['URL'],
            token=config['INFLUX']['TOKEN'],
            org=config['INFLUX']['ORG'],
            debug=config['INFLUX'].get('DEBUG', '0') != '0')
        self.write_api = self.client.write_api(write_options=ASYNCHRONOUS)

    @classmethod
    def create_idb_point(cls, tags, fields, ts=None, measurement_name=None):
        if measurement_name is None:
            measurement_name = " ".join(tags.values()).replace(" ", "_").lower()
        if ts is None:
            ts = time.time_ns()
        p = Point(measurement_name)
        for tag, value in tags.items():
            p.tag(tag.lower().replace(" ", "_"), value)
        for field, value in fields.items():
            p.field(field.lower().replace(" ", "_"), value)
        p.time(ts)
        return p

    def write_points(self, bucket, points):
        self.write_api.write(bucket, record=points, write_precision=WritePrecision.NS)
