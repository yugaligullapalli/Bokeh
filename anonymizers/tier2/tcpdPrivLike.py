from random import Random

rng = Random()

def seed(seed):
    rng.seed(seed)

def anonymize(lon, lat, numDecimals = 3):
    return (_anonymize(lon, 180, numDecimals), _anonymize(lat, 90, numDecimals))

prefixMap = {}

def _anonymize(value, bound, numDecimals):
    if bound not in prefixMap:
        prefixMap[bound] = {}

    prefix = int(value)
    if prefix not in prefixMap[bound]:
        prefixMap[bound][prefix] = rng.randint(-bound, bound)

    return prefixMap[bound][prefix] + round(rng.random(), numDecimals)