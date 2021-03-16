import time
import json

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from config import config


class KSEM:
    tags = dict(
        deviceName='KSEM',
        deviceType='SmartEnergyMeter'
    )

    def __init__(self):
        client = ModbusTcpClient(config['KSEM']['IP'], port=config['KSEM']['PORT'])
        client.connect()
        self._client = client

    def _read(self, addr, count, unit):
        holdings = self._client.read_holding_registers(addr, count, unit=unit)
        return BinaryPayloadDecoder.fromRegisters(holdings.registers, byteorder=Endian.Big, wordorder=Endian.Big)

    def _read_int32(self, addr, multiplier):
        return self._read(addr, 2, 71).decode_32bit_int() * multiplier

    def _read_uint64(self, addr, multiplier):
        return self._read(addr, 4, 71).decode_64bit_uint() * multiplier

    def _read_u32(self, addr, multiplier):
        return self._read(addr, 2, 71).decode_32bit_uint() * multiplier

    def terminate(self):
        self._client.close()

    def get_results(self):
        results = []
        for addr, tags, multiplier in [
            (0, dict(type="active", unit="power", option="purchase"), 0.1),
            (2, dict(type="active", unit="power", option="sell"), 0.1),
            (4, dict(type="reactive", unit="power", option="purchase"), 0.1),
            (6, dict(type="reactive", unit="power", option="sell"), 0.1),
            (16, dict(type="apparent", unit="power", option="purchase"), 0.1),
            (18, dict(type="apparent", unit="power", option="sell"), 0.1),
            (26, dict(type="supply frequency",), 0.001),
            (40, dict(type="active", unit="power", option="purchase", phase="1"), 0.1),
            (42, dict(type="active", unit="power", option="sell", phase="1"), 0.1),
            (44, dict(type="reactive", unit="power", option="purchase", phase="1"), 0.1),
            (46, dict(type="reactive", unit="power", option="sell", phase="1"), 0.1),
            (56, dict(type="apparent", unit="power", option="purchase", phase="1"), 0.1),
            (58, dict(type="apparent", unit="power", option="sell", phase="1"), 0.1),
            (60, dict(type="current", phase="1"), 0.001),
            (62, dict(type="voltage", phase="1"), 0.001),
            (64, dict(type="power factor", phase="1"), 0.001),
            (80, dict(type="active", unit="power", option="purchase", phase="2"), 0.1),
            (82, dict(type="active", unit="power", option="sell", phase="2"), 0.1),
            (84, dict(type="reactive", unit="power", option="purchase", phase="2"), 0.1),
            (86, dict(type="reactive", unit="power", option="sell", phase="2"), 0.1),
            (96, dict(type="apparent", unit="power", option="purchase", phase="2"), 0.1),
            (98, dict(type="apparent", unit="power", option="sell", phase="2"), 0.1),
            (100, dict(type="current", phase="2"), 0.001),
            (102, dict(type="voltage", phase="2"), 0.001),
            (120, dict(type="active", unit="power", option="purchase", phase="3"), 0.1),
            (122, dict(type="active", unit="power", option="sell", phase="3"), 0.1),
            (124, dict(type="reactive", unit="power", option="purchase", phase="3"), 0.1),
            (126, dict(type="reactive", unit="power", option="sell", phase="3"), 0.1),
            (136, dict(type="apparent", unit="power", option="purchase", phase="3"), 0.1),
            (138, dict(type="apparent", unit="power", option="sell", phase="3"), 0.1),
            (140, dict(type="current", phase="3"), 0.001),
            (142, dict(type="voltage", phase="3"), 0.001),
        ]:
            results.append(dict(value=self._read_u32(addr, multiplier), ts=time.time_ns(), tags=tags))

        for addr, tags in [
            (24, dict(type="power factor", phase="1")),
            (104, dict(type="power factor", phase="2")),
            (144, dict(type="power factor", phase="3"))
        ]:
            results.append(dict(value=self._read_int32(addr, 0.001), ts=time.time_ns(), tags=tags))

        for addr, tags in [
            (512, dict(type="active", unit="energy", option="purchase")),
            (516, dict(type="active", unit="energy", option="sell")),
            (520, dict(type="reactive", unit="energy", option="purchase")),
            (524, dict(type="reactive", unit="energy", option="sell")),
            (544, dict(type="apparent", unit="energy", option="purchase")),
            (548, dict(type="apparent", unit="energy", option="sell")),
            (592, dict(type="active", unit="energy", option="purchase", phase="1")),
            (596, dict(type="active", unit="energy", option="sell", phase="1")),
            (600, dict(type="reactive", unit="energy", option="purchase", phase="1")),
            (604, dict(type="reactive", unit="energy", option="sell", phase="1")),
            (624, dict(type="apparent", unit="energy", option="purchase", phase="1")),
            (628, dict(type="apparent", unit="energy", option="sell", phase="1")),
            (672, dict(type="active", unit="energy", option="purchase", phase="2")),
            (676, dict(type="active", unit="energy", option="sell", phase="2")),
            (680, dict(type="reactive", unit="energy", option="purchase", phase="2")),
            (684, dict(type="reactive", unit="energy", option="sell", phase="2")),
            (704, dict(type="apparent", unit="energy", option="purchase", phase="2")),
            (708, dict(type="apparent", unit="energy", option="sell", phase="2")),
            (752, dict(type="active", unit="energy", option="purchase", phase="3")),
            (756, dict(type="active", unit="energy", option="sell", phase="3")),
            (760, dict(type="reactive", unit="energy", option="purchase", phase="3")),
            (764, dict(type="reactive", unit="energy", option="sell", phase="3")),
            (784, dict(type="apparent", unit="energy", option="purchase", phase="3")),
            (788, dict(type="apparent", unit="energy", option="sell", phase="3")),

        ]:
            results.append(dict(value=self._read_uint64(addr, 0.1), ts=time.time_ns(), tags=tags))

        return results


if __name__ == "__main__":
    ksem = KSEM()
    result = ksem.get_results()
    print(json.dumps(result, indent=2))
    ksem.terminate()
