import json
import time

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

    def get_results(self, ts=None):
        ts = ts or time.time_ns()
        results = []
        for addr, measurement, multiplier in [
            (0, "active_power_purchase", 0.1),
            (2, "active_power_sell", 0.1),
            (4, "reactive_power_purchase", 0.1),
            (6, "reactive_power_sell", 0.1),
            (16, "apparent_power_purchase", 0.1),
            (18, "apparent_power_sell", 0.1),
            (26, "supply frequency", 0.001),
            (40, "active_power_purchase_1", 0.1),
            (42, "active_power_sell_1", 0.1),
            (44, "reactive_power_purchase_1", 0.1),
            (46, "reactive_power_sell_1", 0.1),
            (56, "apparent_power_purchase_1", 0.1),
            (58, "apparent_power_sell_1", 0.1),
            (60, "current_1", 0.001),
            (62, "voltage_1", 0.001),
            (64, "power factor_1", 0.001),
            (80, "active_power_purchase_2", 0.1),
            (82, "active_power_sell_2", 0.1),
            (84, "reactive_power_purchase_2", 0.1),
            (86, "reactive_power_sell_2", 0.1),
            (96, "apparent_power_purchase_2", 0.1),
            (98, "apparent_power_sell_2", 0.1),
            (100, "current_2", 0.001),
            (102, "voltage_2", 0.001),
            (120, "active_power_purchase_3", 0.1),
            (122, "active_power_sell_3", 0.1),
            (124, "reactive_power_purchase_3", 0.1),
            (126, "reactive_power_sell_3", 0.1),
            (136, "apparent_power_purchase_3", 0.1),
            (138, "apparent_power_sell_3", 0.1),
            (140, "current_3", 0.001),
            (142, "voltage_3", 0.001),
        ]:
            results.append(dict(value=self._read_u32(addr, multiplier), ts=ts, measurement=measurement))

        for addr, measurement in [
            (24, "power_factor_1"),
            (104, "power_factor_2"),
            (144, "power_factor_3")
        ]:
            results.append(dict(value=self._read_int32(addr, 0.001), ts=ts, measurement=measurement))

        for addr, measurement in [
            (512, "active_energy_purchase"),
            (516, "active_energy_sell"),
            (520, "reactive_energy_purchase"),
            (524, "reactive_energy_sell"),
            (544, "apparent_energy_purchase"),
            (548, "apparent_energy_sell"),
            (592, "active_energy_purchase_1"),
            (596, "active_energy_sell_1"),
            (600, "reactive_energy_purchase_1"),
            (604, "reactive_energy_sell_1"),
            (624, "apparent_energy_purchase_1"),
            (628, "apparent_energy_sell_1"),
            (672, "active_energy_purchase_2"),
            (676, "active_energy_sell_2"),
            (680, "reactive_energy_purchase_2"),
            (684, "reactive_energy_sell_2"),
            (704, "apparent_energy_purchase_2"),
            (708, "apparent_energy_sell_2"),
            (752, "active_energy_purchase_3"),
            (756, "active_energy_sell_3"),
            (760, "reactive_energy_purchase_3"),
            (764, "reactive_energy_sell_3"),
            (784, "apparent_energy_purchase_3"),
            (788, "apparent_energy_sell_3"),

        ]:
            results.append(dict(value=self._read_uint64(addr, 0.1), ts=ts, measurement=measurement))

        return results


if __name__ == "__main__":
    ksem = KSEM()
    result = ksem.get_results()
    print(json.dumps(result, indent=2))
    ksem.terminate()
