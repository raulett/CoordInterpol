from exif import Image
from GetSpatialData import openGpxFiles
import coordFunction

from datetime import *
from tkinter import filedialog

timeshift = -0.75

tableLonLatAlt = openGpxFiles.openGpxFiles()
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)

photoFileNames = filedialog.askopenfilenames()

for photoFileName in photoFileNames:
    file = open(photoFileName, 'rb')
    image = Image(file)
    file.close()
    print(dir(image))
    print(image.gps_longitude_ref)
    print(image.gps_longitude)
    print(image.gps_altitude)
    print(image.gps_altitude_ref)
    picDateTime = image.datetime + timedelta(seconds=timeshift)
    photoUnixTimestamp = datetime.strptime(picDateTime, '%Y:%m:%d %H:%M:%S').timestamp()
    print(image.datetime)
    print(image.datetime_digitized)
    print(picDateTime)
    print(photoUnixTimestamp)
    latLonAlt = LatLonAltInterpolFunc.getLonLatAlt(photoUnixTimestamp)
    degLat = int(latLonAlt[0])
    minLat = int((latLonAlt[0] - degLat) * 60)
    secLat = ((latLonAlt[0] - degLat) * 60) - minLat
    lat = (degLat, minLat, secLat)
    degLon = int(latLonAlt[0])
    minLon = int((latLonAlt[0] - degLat) * 60)
    secLat = ((latLonAlt[0] - degLat) * 60) - minLat
    lat = (degLat, minLat, secLat)