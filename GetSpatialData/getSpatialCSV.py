from datetime import *
from tkinter import filedialog
import sys

def getSpatialCSV(filesCSV, delimiter):

    counter = 0
    csv_points = []
    timeStampCounter = 0
    datetimeIndex = -1
    lonIndex = -1
    latIndex = -1
    altIndex = -1
    dateTimeFormat = "%d-%m-%YT%H:%M:%S"

    for file in filesCSV:
        csv_file = open(file, 'r', encoding="utf_8_sig")
        lines = csv_file.readlines()
        elementIndex = 0
        fieldNameCount = 0
        for element in lines[0].replace('\n', '').split(delimiter):
            if element == "DATETIME":
                datetimeIndex = elementIndex
                fieldNameCount += 1
            if element == "LON":
                lonIndex = elementIndex
                fieldNameCount += 1
            if element == "LAT":
                latIndex = elementIndex
                fieldNameCount += 1
            if element == "ALT":
                altIndex = elementIndex
                fieldNameCount += 1
            elementIndex += 1

        if fieldNameCount < 4:
            sys.exit("No DATETIME, LON, LAT or ALT field in coord files")
        else:
            print("DateTime index: {0}, Lon: {1}, Lat: {2}, Alt: {3}".format(datetimeIndex, lonIndex,
                                                                             latIndex, altIndex))

        for line in lines:
            value = line.replace('\n', '').split(delimiter)
            try:
                dateTimeUT = datetime.strptime(value[datetimeIndex], dateTimeFormat).timestamp()
            except:
                print("Error with parsing time from {0} element".format(value[datetimeIndex]))
                continue
            if (timeStampCounter != dateTimeUT):
                timeStampCounter = dateTimeUT

                csv_points.append((float(value[lonIndex]), float(value[latIndex]),
                                   float(value[altIndex]), float(dateTimeUT)))
            counter += 1
        csv_file.close()

    print("there is {0} coord points".format(counter))
    def getKey(item):
        return item[3]
    csv_points = sorted(csv_points, key = getKey)
    return csv_points