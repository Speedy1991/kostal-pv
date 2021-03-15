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
    def create_idb_point(cls, measurement_name, tags, fields, ts=None):
        if ts is None:
            ts = time.time_ns()
        p = Point(measurement_name)
        for tag, value in tags:
            p.tag(tag, value)
        for field, value in fields:
            p.field(field, value)
        p.time(ts)
        return p

    def write_points(self, bucket, points):
        self.write_api.write(bucket, record=points, write_precision=WritePrecision.NS)
