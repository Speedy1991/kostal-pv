import time
import json

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from config import config


class KSEM:

    name = 'ksem'
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
            (0, dict(type="Active", unit="power", pole="+"), 0.1),
            (2, dict(type="Active", unit="power", pole="-"), 0.1),
            (4, dict(type="Reactive", unit="power", pole="+"), 0.1),
            (6, dict(type="Reactive", unit="power", pole="-"), 0.1),
            (16, dict(type="Apparent", unit="power", pole="+"), 0.1),
            (18, dict(type="Apparent", unit="power", pole="-"), 0.1),
            (26, dict(type="Supply frequency",), 0.001),
            (40, dict(type="Active", unit="power", pole="+", phase="1"), 0.1),
            (42, dict(type="Active", unit="power", pole="-", phase="1"), 0.1),
            (44, dict(type="Reactive", unit="power", pole="+", phase="1"), 0.1),
            (46, dict(type="Reactive", unit="power", pole="-", phase="1"), 0.1),
            (56, dict(type="Apparent", unit="power", pole="+", phase="1"), 0.1),
            (58, dict(type="Apparent", unit="power", pole="-", phase="1"), 0.1),
            (60, dict(type="Current", phase="1"), 0.001),
            (62, dict(type="Voltage", phase="1"), 0.001),
            (64, dict(type="Power factor", phase="1"), 0.001),
            (80, dict(type="Active", unit="power", pole="+", phase="2"), 0.1),
            (82, dict(type="Active", unit="power", pole="-", phase="2"), 0.1),
            (84, dict(type="Reactive", unit="power", pole="+", phase="2"), 0.1),
            (86, dict(type="Reactive", unit="power", pole="-", phase="2"), 0.1),
            (96, dict(type="Apparent", unit="power", pole="+", phase="2"), 0.1),
            (98, dict(type="Apparent", unit="power", pole="-", phase="2"), 0.1),
            (100, dict(type="Current", phase="2"), 0.001),
            (102, dict(type="Voltage", phase="2"), 0.001),
            (120, dict(type="Active", unit="power", pole="+", phase="3"), 0.1),
            (122, dict(type="Active", unit="power", pole="-", phase="3"), 0.1),
            (124, dict(type="Reactive", unit="power", pole="+", phase="3"), 0.1),
            (126, dict(type="Reactive", unit="power", pole="-", phase="3"), 0.1),
            (136, dict(type="Apparent", unit="power", pole="+", phase="3"), 0.1),
            (138, dict(type="Apparent", unit="power", pole="-", phase="3"), 0.1),
            (140, dict(type="Current", phase="3"), 0.001),
            (142, dict(type="Voltage", phase="3"), 0.001),
        ]:
            results.append(dict(value=self._read_u32(addr, multiplier), name=" ".join(tags.values()), ts=time.time_ns(), tags=tags))

        for addr, tags in [
            (24, dict(type="Power factor", phase="1")),
            (104, dict(type="Power factor", phase="2")),
            (144, dict(type="Power factor", phase="3"))
        ]:
            results.append(dict(value=self._read_int32(addr, 0.001), name=" ".join(tags.values()), ts=time.time_ns(), tags=tags))

        for addr, tags in [
            (512, dict(type="Active", unit="energy", pole="+")),
            (516, dict(type="Active", unit="energy", pole="-")),
            (520, dict(type="Reactive", unit="energy", pole="+")),
            (524, dict(type="Reactive", unit="energy", pole="-")),
            (544, dict(type="Apparent", unit="energy", pole="+")),
            (548, dict(type="Apparent", unit="energy", pole="-")),
            (592, dict(type="Active", unit="energy", pole="+", phase="1")),
            (596, dict(type="Active", unit="energy", pole="-", phase="1")),
            (600, dict(type="Reactive", unit="energy", pole="+", phase="1")),
            (604, dict(type="Reactive", unit="energy", pole="-", phase="1")),
            (624, dict(type="Apparent", unit="energy", pole="+", phase="1")),
            (628, dict(type="Apparent", unit="energy", pole="-", phase="1")),
            (672, dict(type="Active", unit="energy", pole="+", phase="2")),
            (676, dict(type="Active", unit="energy", pole="-", phase="2")),
            (680, dict(type="Reactive", unit="energy", pole="+", phase="2")),
            (684, dict(type="Reactive", unit="energy", pole="-", phase="2")),
            (704, dict(type="Apparent", unit="energy", pole="+", phase="2")),
            (708, dict(type="Apparent", unit="energy", pole="-", phase="2")),
            (752, dict(type="Active", unit="energy", pole="+", phase="3")),
            (756, dict(type="Active", unit="energy", pole="-", phase="3")),
            (760, dict(type="Reactive", unit="energy", pole="+", phase="3")),
            (764, dict(type="Reactive", unit="energy", pole="-", phase="3")),
            (784, dict(type="Apparent", unit="energy", pole="+", phase="3")),
            (788, dict(type="Apparent", unit="energy", pole="-", phase="3")),

        ]:
            results.append(dict(value=self._read_uint64(addr, 0.1), name=" ".join(tags.values()), ts=time.time_ns(), tags=tags))

        return results


if __name__ == "__main__":
    ksem = KSEM()
    result = ksem.get_results()
    print(json.dumps(result, indent=2))
    ksem.terminate()
