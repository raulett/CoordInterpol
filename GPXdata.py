class GPXdata:
    def __init__(self):
        self.Points = []

    def addPoint(self, lat, lon, time, data, elevation):
        self.Points.append(GPXPoint(lat, lon, time, data, elevation))


class GPXPoint:
    def __init__(self, lat, lon, time, data, elevation):
        self.lat = lat
        self.lon = lon
        self.time = time
        self.data = data
        self.elevation = elevation

