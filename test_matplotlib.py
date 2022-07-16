from getMagnDataV2 import getMagnData
from common.SplinesArray import ValueNotFoundException
from common.LinearSpline import ImpossibleException
import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from GetSpatialData import openGpxFiles


filenames = [r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\flights\g1magn\20210907\data\1-7\2021-09-07_10-39-20.txt']
gpxFiles = [r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\flights\g1magn\20210907\data\1-7\LOGS\00000001.BIN.gpx',
            r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\flights\g1magn\20210907\data\1-7\LOGS\00000002.BIN.gpx',
            r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\flights\g1magn\20210907\data\1-7\LOGS\00000003.BIN.gpx',
            r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\flights\g1magn\20210907\data\1-7\LOGS\00000004.BIN.gpx',
            r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\flights\g1magn\20210907\data\1-7\LOGS\00000005.BIN.gpx',
            r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\flights\g1magn\20210907\data\1-7\LOGS\00000006.BIN.gpx',
            r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\flights\g1magn\20210907\data\1-7\LOGS\00000007.BIN.gpx',]
magn_points = getMagnData(filenames, '%m.%d.%yT%H:%M:%S,%f')
gpx_functions = openGpxFiles.openGpxFiles(gpxFiles)

timelag = 0
fig, ax = plt.subplots()
fig.set_size_inches(14, 8)
ax.xaxis.axis_date()
x = [datetime.datetime.fromtimestamp(point[0]+timelag) for point in magn_points]
dates = matplotlib.dates.date2num(x)
y = np.array([int(point[1])/1000 for point in magn_points])
hist, bin_edges = np.histogram(y, bins=76)
max_el_index = hist.argmax(axis=0)
print(hist)
print(bin_edges)
print(max_el_index)
# median_val = (bin_edges[max_el_index] + bin_edges[max_el_index+1])/2
class_delta = bin_edges[max_el_index+1]-bin_edges[max_el_index]
low_lim = bin_edges[max_el_index] - class_delta/10
high_lim = bin_edges[max_el_index] + class_delta + class_delta/10
plt.ylim(low_lim, high_lim)
colors = []

for point in magn_points:
    date = datetime.datetime.fromtimestamp(point[0]+timelag)
    date_pnt = matplotlib.dates.date2num(date)
    try:
        lon = gpx_functions[0].get_value(point[0]+timelag)
        colors.append('r')
        # plt.plot(date_pnt, int(point[1]) / 1000, 'ro', markersize =1)
    except Exception as e:
        colors.append('b')
        # plt.plot(date_pnt, int(point[1]) / 1000, 'bo', markersize =1)
colors = np.array(colors)

# plt.plot(dates, y, color=colors,  marker='o', markersize=1)

plt.scatter(dates, y, color=colors, s=0.5)
plt.show()