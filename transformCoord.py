# Показывает графический интерфейс выбора нескольких gpx файлов и на выходе возвращает массив кортежей, представляющих
# координатные точки вида (lon, lat, alt, nixTimstamp). Массив отсортирован по времени.
# OpenMagnFile Вытаскивает точки из файла сагнитного поля и в виде (lon, lat, elev, timestamp);

from datetime import *
from tkinter import filedialog
import gpxpy
import gpxpy.gpx
import datetime
from datetime import *


def openGpxFiles():
    filesCoord = filedialog.askopenfilenames(title = ("Choose gpx coord files"), filetypes = (("Template files", "*.gpx"),("All files", "*.*")))
    counter = 0
    gpx_points = []
    for file in filesCoord:
        gpx_file = open(file, 'r', encoding="utf_8_sig")
        gpx = gpxpy.parse(gpx_file)

        for route in gpx.routes:
            print('Route:')
            for point in route.points:
                counter+=1
        # for waypoint in gpx.waypoints:
        #     gpx_points.append(tuple((waypoint.longitude, waypoint.latitude, waypoint.elevation,
        #                              (waypoint.time + timedelta(hours=8)).timestamp())))
        #     counter += 1
        pointtime = 0
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    stamp = (point.time + timedelta(hours=0)).timestamp()
                    if (stamp != pointtime):
                        gpx_points.append(tuple((point.longitude, point.latitude, point.elevation, stamp)))
                        pointtime = stamp
                        counter += 1
        gpx_file.close()

    print(counter)
    def getKey(item):
        return item[3]
    gpx_points = sorted(gpx_points, key=getKey)
    return gpx_points

def openMagnFiles():
    filesCoord = filedialog.askopenfilenames(title=("Choose magn coord files"),
                                             filetypes=(("magnetic", "*.txt"), ("All files", "*.*")))
    counter = 0
    gpx_points = []
    for file in filesCoord:
        gps_file = open(file, 'r')
        lines = gps_file.readlines()
        for line in lines:
            line = line.replace('\n', '').split('\t')
            try:
                lon = float(line[4])
                lat = float(line[3])
                elev = float(line[5])
                time = int(datetime.strptime(line[2], "%Y-%m-%dT%H:%M:%S").timestamp())
            except ValueError:
                continue

            gpx_points.append((lon, lat, elev, time))
            counter += 1
        gps_file.close()

    def getKey(item):
        return item[3]
    gpx_points = sorted(gpx_points, key=getKey)
    return gpx_points

