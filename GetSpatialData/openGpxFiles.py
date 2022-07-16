# Показывает графический интерфейс выбора нескольких gpx файлов и на выходе возвращает массив кортежей, представляющих
# координатные точки вида (lon, lat, alt, UnixTimstamp). Массив отсортирован по времени.
import datetime
from datetime import *
from tkinter import filedialog
import gpxpy
import gpxpy.gpx
from common.SplinesArray import *



def openGpxFiles(coordFileNames):
    filesCoord = coordFileNames
    counter = 0
    gpx_points = []

    lon_function = SplinesArray()
    lat_function = SplinesArray()
    alt_function = SplinesArray()
    timeStampCounter = 0
    files_count = len(filesCoord)
    files_counter = 1
    def getKey(item):
        return item[0]
    for file in filesCoord:
        lon_points = []
        lat_points = []
        alt_points = []
        print("open GPX. Handle {} file {} from {}. ".format(file, files_counter, files_count))
        files_counter += 1
        gpx_file = open(file, 'r', encoding="utf_8_sig")
        gpx = gpxpy.parse(gpx_file)

        # for route in gpx.routes:
        #     print('Route:')
        #     for point in route.points:
        #         counter+=1
        # for point in gpx.trackpoints:
        #     print('Route:')
        #     for point in route.points:
        #         counter+=1
        # for waypoint in gpx.waypoints:
        #     gpx_points.append(tuple((waypoint.longitude, waypoint.latitude, waypoint.elevation,
        #                              (waypoint.time + timedelta(hours=8)).timestamp())))
        #     counter += 1

        for track in gpx.tracks:
            #print("gpx track {}\n".format(track))
            for segment in track.segments:
                #print("gpx segment {}\n".format(segment))
                for point in segment.points:
                    #print("gpx point {}\n".format(point))
                    if (timeStampCounter != int((point.time + datetime.timedelta(hours=0)).timestamp())):
                        #print("timestamp_counter = {}, point.time = {}".format(timeStampCounter, point.time))
                        timeStampCounter = int((point.time + datetime.timedelta(hours=0)).timestamp())
                        gpx_points.append(tuple((point.longitude, point.latitude, point.elevation, timeStampCounter)))
                        lon_points.append((timeStampCounter, point.longitude))
                        lat_points.append((timeStampCounter, point.latitude))
                        alt_points.append((timeStampCounter, point.elevation))
                        counter += 1
        lon_points = sorted(lon_points, key=getKey)
        lat_points = sorted(lat_points, key=getKey)
        alt_points = sorted(alt_points, key=getKey)
        lon_function.add_spline(lon_points)
        lat_function.add_spline(lat_points)
        alt_function.add_spline(alt_points)
        gpx_file.close()

    print(counter)
    def getKey(item):
        return item[3]
    #print("GPX sort started.")
    gpx_points = sorted(gpx_points, key=getKey)
    #print("GPX sorted.")
    return lon_function, lat_function, alt_function, gpx_points
