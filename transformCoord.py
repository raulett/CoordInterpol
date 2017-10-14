from datetime import *
from tkinter import filedialog
import gpxpy
import gpxpy.gpx



def openGpxFiles():
    filesCoord = filedialog.askopenfilenames(title = ("Choose gpx coord files"), filetypes = (("Template files", "*.gpx"),("All files", "*.*")))
    counter = 0
    gpx_points = []
    for file in filesCoord:
        gpx_file = open(file, 'r')
        gpx = gpxpy.parse(gpx_file)

        for route in gpx.routes:
            print('Route:')
            for point in route.points:
                print('Route Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
                counter+=1
        for waypoint in gpx.waypoints:
            print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))
            counter += 1
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    print('Track Point at ({0},{1}) -> {2}, {3}'.format(point.latitude, point.longitude, point.elevation, point.time.timestamp()))
                    gpx_points.append(tuple((point.longitude, point.latitude, point.elevation, (point.time+timedelta(hours=8)).timestamp())))
                    counter += 1
        gpx_file.close()

    print(counter)
    def getKey(item):
        return item[3]
    gpx_points = sorted(gpx_points, key=getKey)
    return gpx_points
