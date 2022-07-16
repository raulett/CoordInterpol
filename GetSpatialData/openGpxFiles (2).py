# Показывает графический интерфейс выбора нескольких gpx файлов и на выходе возвращает массив кортежей, представляющих
# координатные точки вида (lon, lat, alt, UnixTimstamp). Массив отсортирован по времени.

from datetime import *
from tkinter import filedialog
import gpxpy
import gpxpy.gpx



def openGpxFiles():
    filesCoord = filedialog.askopenfilenames(title = ("Choose gpx coord files"), filetypes = (("Template files", "*.gpx"),("All files", "*.*")))
    counter = 0
    gpx_points = []
    timeStampCounter = 0
    files_count = len(filesCoord)
    files_counter = 1
    for file in filesCoord:
        print("open GPX. Handle file {} from {}. ".format(files_counter, files_count))
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
            for segment in track.segments:
                for point in segment.points:
                    if (timeStampCounter != point.time):
                        timeStampCounter = point.time
                        gpx_points.append(tuple((point.longitude, point.latitude, point.elevation,
                                             (point.time + timedelta(hours=0, seconds=0)).timestamp())))
                        counter += 1
        gpx_file.close()

    print(counter)
    def getKey(item):
        return item[3]
    print("GPX sort started.")
    gpx_points = sorted(gpx_points, key=getKey)
    print("GPX sorted.")
    return gpx_points
