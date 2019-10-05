import bitstring
import hmac
import hashlib
from random import Random
rng = Random()


keys = [rng.getrandbits(512).to_bytes(64, byteorder = 'little') for x in range(0, 31)]

def seed(seed):
    global keys
    keys = [rng.getrandbits(512).to_bytes(64, byteorder = 'little') for x in range(0, 31)]

def anonymize(longitude, latitude, numDecimals = 3):
    return (_anonymize(shiftToPositive(longitude), numDecimals), _anonymize(shiftToPositive(latitude), numDecimals))

def _anonymize(value, numDecimals):
    valueAsInt = int(value * 10 ** numDecimals)
    anonymizedBitstring = bitstring.BitArray(length = 32)
    anonymizedBitstring.set(getBit(valueAsInt, 0), 0)
    for i in range(1, 32):
        mac = hmac.new(keys[i - 1], getPaddedBytes(valueAsInt, i), hashlib.md5)
        lsb = bool(int(mac.digest()[-1]) & 0x1)
        anonymizedBitstring.set(lsb ^ getBit(valueAsInt, i), i)
    return anonymizedBitstring.int / (10.0 ** numDecimals)

def shiftToPositive(value):
    return value + 180

def getPaddedBytes(value, numBits):
    valueBits = bitstring.Bits(int = value, length = 32)
    result = bitstring.BitArray(int = numBits, length = (512-numBits))
    result.prepend(valueBits[0:numBits])
    return result.bytes

def getBit(value, bitIndex):
    return bitstring.Bits(int = value, length = 32)[bitIndex]