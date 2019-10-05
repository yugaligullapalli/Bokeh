from math import radians, sin, cos, asin, sqrt

class DistanceTracker:
    def __init__(self, inner, file):
        self.inner = inner
        self.file = file
    
    def seed(self, value):
        self.inner.seed(value)

    def anonymize(self, longitude, latitude, decimals):
        lon2, lat2 = self.inner.anonymize(longitude, latitude, decimals)
        self.file.write('{}\n'.format(abs(haversine(longitude, latitude, lon2, lat2))))
        return lon2, lat2
    
    def flush(self):
        self.file.flush()
        self.file.close()


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 * 1000 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
