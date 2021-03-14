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

    def _read_u16_1(self, addr, name, multiplier):
        result = self._read(addr, 1, 71).decode_16bit_uint()
        return name, addr, result * multiplier, time.time()

    def _read_int32(self, addr, name, multiplier):
        result = self._read(addr, 2, 71).decode_32bit_int()
        return name, addr, result * multiplier, time.time()

    def _read_uint64(self, addr, name, multiplier):
        result = self._read(addr, 4, 71).decode_64bit_uint()
        return name, addr, result * multiplier, time.time()

    def _read_u32(self, addr, name, multiplier):
        result = self._read(addr, 2, 71).decode_32bit_uint()
        return name, addr, result * multiplier, time.time()

    def terminate(self):
        self._client.close()

    def get_results(self):
        results = []
        for addr, name, multiplier in [
            (0, "Active power+", 0.1),
            (2, "Active power-", 0.1),
            (4, "Reactive power+", 0.1),
            (6, "Reactive power-", 0.1),
            (16, "Apparent power+", 0.1),
            (18, "Apparent power-", 0.1),
            (26, "Supply frequency", 0.001),
            (40, "Active power+ (L1)", 0.1),
            (42, "Active power- (L1)", 0.1),
            (44, "Reactive power+ (L1)", 0.1),
            (46, "Reactive power- (L1)", 0.1),
            (56, "Apparent power+ (L1)", 0.1),
            (58, "Apparent power- (L1)", 0.1),
            (60, "Current (L1)", 0.001),
            (62, "Voltage (L1)", 0.001),
            (64, "Power factor (L1)", 0.001),
            (80, "Active power+ (L2)", 0.1),
            (82, "Active power- (L2)", 0.1),
            (84, "Reactive power+ (L2)", 0.1),
            (86, "Reactive power- (L2)", 0.1),
            (96, "Apparent power+ (L2)", 0.1),
            (98, "Apparent power- (L2)", 0.1),
            (100, "Current (L2)", 0.001),
            (102, "Voltage (L2)", 0.001),
            (120, "Active power+ (L3)", 0.1),
            (122, "Active power- (L3)", 0.1),
            (124, "Reactive power+ (L3)", 0.1),
            (126, "Reactive power- (L3)", 0.1),
            (136, "Apparent power+ (L3)", 0.1),
            (138, "Apparent power- (L3)", 0.1),
            (140, "Current (L3)", 0.001),
            (142, "Voltage (L3)", 0.001),
        ]:
            results.append(self._read_u32(addr, name, multiplier))

        for addr, name in [
            (24, "Power factor (L1)"),
            (104, "Power factor (L2)"),
            (144, "Power factor (L3)")
        ]:
            results.append(self._read_int32(addr, name, 0.001))

        for addr, name in [
            (512, "Active energy+"),
            (516, "Active energy-"),
            (520, "Reactive energy+"),
            (524, "Reactive energy-"),
            (544, "Apparent energy+"),
            (548, "Apparent energy-"),
            (592, "Active energy+ (L1)"),
            (596, "Active energy- (L1)"),
            (600, "Reactive energy+ (L1)"),
            (604, "Reactive energy- (L1)"),
            (624, "Apparent energy+ (L1)"),
            (628, "Apparent energy- (L1)"),
            (672, "Active energy+ (L2)"),
            (676, "Active energy- (L2)"),
            (680, "Reactive energy+ (L2)"),
            (684, "Reactive energy- (L2)"),
            (704, "Apparent energy+ (L2)"),
            (708, "Apparent energy- (L2)"),
            (752, "Active energy+ (L3)"),
            (756, "Active energy- (L3)"),
            (760, "Reactive energy+ (L3)"),
            (764, "Reactive energy- (L3)"),
            (784, "Apparent energy+ (L3)"),
            (788, "Apparent energy- (L3)"),

        ]:
            results.append(self._read_uint64(addr, name, 0.1))

        results.append(self._read_u16_1(8192, 'ManufacturerID', 1))
        return [{'name': t[0], 'register': t[1], 'value': t[2], 'ts': t[3]} for t in results]


if __name__ == "__main__":
    ksem = KSEM()
    result = ksem.get_results()
    print(json.dumps(result, indent=2))
    ksem.terminate()
