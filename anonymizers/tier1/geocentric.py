from random import Random
from pyproj import Proj

rng = Random()

ellipsoids = ["delmbr", "andrae", "intl"]
ellipsoidZ = ellipsoids[rng.randint(0, len(ellipsoids) - 1)]
projBack = Proj(ellps = ellipsoidZ, proj='utm')

def seed(seed):
    global ellipsoidZ, projBack
    rng.seed(seed)
    ellipsoidZ = ellipsoids[rng.randint(0, len(ellipsoids) - 1)]
    projBack = Proj(ellps = ellipsoidZ, proj='utm')

def anonymize(longitude, latitude, _):
    ellipsoidA = ellipsoids[rng.randint(0, len(ellipsoids) - 1)]
    while ellipsoidA == ellipsoidZ:
        ellipsoidA = ellipsoids[rng.randint(0, len(ellipsoids) - 1)]
    projection = Proj(ellps = ellipsoidA, proj='utm')

    x, y = projection(longitude, latitude)
    return projBack(x, y, inverse=True)
