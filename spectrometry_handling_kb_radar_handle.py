# Берет файлы *.dat из спектрометра shproto и компанует их в один TAB separated text и расчитывает каналы U, Th, K, на основе данных из блока констант ниже.

from tkinter import filedialog
import numpy as np
import os
import datetime
from GetSpatialData import openGpxFiles
import coordFunction
from common.SplinesArray import *

timeshift = 0
spectrum_size = 8192

def getDATdataFromFile(file):

    # Calibration coefficient kx+b, calculate in channels
    #Calibration kb_radar_4096_01
    k = 2.73958333
    b = 25.66666667


    # u1 = (int(k*609+b), int(k*619+b))
    u1 = (int(k * 2035 + b), int(k * 2280 + b)) #корректировка по графику 2.2
    u2 = (int(k*1055+b), int(k*1185+b)) #1120
    u3 = (int(k*1670+b), int(k*1830+b)) #1,76
    th1 = (int(k*875+b), int(k*1010+b)) #910
    th2 = (int(k*2356+b), int(k*2480+b)) #2.4
    K = (int(k*1340+b), int(k*1535+b)) #1459 K40
    integral = (int(k*400+b), int(k*2810+b))

    spectre_array = np.zeros(spectrum_size, np.uint32)
    fileDAT = open(file, 'r', encoding='ANSI')
    lines = fileDAT.readlines()
    spectreRecords = []
    linesLen = len(lines)

    #old
    datetime_ExpoTime_tuple = os.path.basename(fileDAT.name).split('.')[0].split('_')[1: 4]
    # datetime_ExpoTime_tuple = os.path.basename(fileDAT.name).split('.')[0].split('_')[2: 5]
    print("date_time_Expo = {}".format(datetime_ExpoTime_tuple))
    date_time = datetime.datetime.strptime(datetime_ExpoTime_tuple[0]+'T'+datetime_ExpoTime_tuple[1], '%Y%m%dT%H%M%S')+ datetime.timedelta(days=0, seconds=-1)
    print("parse datetime {}".format(date_time))
    expo_time = int(datetime_ExpoTime_tuple[2])

    i = 0
    try:
        for line in lines:

            spectre_array[i] = int(line)
            i += 1
    except IndexError:
        print(file)
        print(line)
        print(i)
        return 1


    U_counts = 0
    Th_counts = 0
    K_counts = 0
    int_counts = 0

    for i in range(u1[0], u1[1] + 1):
        U_counts += spectre_array[i]

    for i in range(u2[0], u2[1] + 1):
        U_counts += spectre_array[i]

    for i in range(u3[0], u3[1] + 1):
        U_counts += spectre_array[i]

    for i in range(th1[0], th1[1] + 1):
        Th_counts += spectre_array[i]

    for i in range(th2[0], th2[1] + 1):
        Th_counts += spectre_array[i]

    for i in range(K[0], K[1] + 1):
        K_counts += spectre_array[i]

    for i in range(integral[0], integral[1] + 1):
        int_counts += spectre_array[i]

    fileDAT.close()
    return (date_time, expo_time, int_counts, U_counts, Th_counts, K_counts, spectre_array)








filesDAT = filedialog.askopenfilenames(title=("Choose Spectre files"),
                                       filetypes=(("Template files", "*.dat"), ("All files", "*.*")))
spectresFile = filedialog.asksaveasfile('w')

i = 0
all_files_num = len(filesDAT)
print("go in gpx parce")
lon_function, lat_function, alt_function, gpx_points = openGpxFiles.openGpxFiles()
print("GPX parced")

print("LON")
lon_function.show_splines()
print("LAT")
lat_function.show_splines()
print("ALT")
alt_function.show_splines()

spectresFile.write('DATETIME\tLON\tLAT\tALT\texpoTime\tINT\tU\tTh\tK\tspectre\n')

for fileDAT in filesDAT:
    if i == 2080:
        pass
    print('handling file {0} of {1}'.format(i + 1, all_files_num))
    data = getDATdataFromFile(fileDAT)
    print("got data from file{}".format(os.path.basename(fileDAT)))
    lon = 0
    lat = 0
    alt = 0
    print("file:{} timestamp: {}, {}".format(os.path.basename(fileDAT), data[0], data[0].timestamp() + timeshift))
    try:
        lon = lon_function.get_value((data[0].timestamp()) + timeshift)
        print("file: {}, time is: {}, lon is: {}".format(os.path.basename(fileDAT), (data[0].timestamp()) + timeshift, lon))
        lat = lat_function.get_value((data[0].timestamp()) + timeshift)
        print("file: {}, time is: {}, lat is: {}".format(os.path.basename(fileDAT), (data[0].timestamp()) + timeshift, lat))
        alt = alt_function.get_value((data[0].timestamp()) + timeshift)
        print("file: {}, time is: {}, alt is: {}".format(os.path.basename(fileDAT), (data[0].timestamp()) + timeshift, alt))
    except ValueNotFoundException:
        print(ValueNotFoundException)
    except ImpossibleException:
        print(ImpossibleException)

    spectresFile.write(data[0].strftime('%d-%m-%YT%H:%M:%S') + '\t' +
                        str(lon) + '\t' +
                        str(lat) + '\t' +
                        str(alt) + '\t' +
                        str(data[1]) + '\t' +
                        str(data[2]) + '\t' +
                        str(data[3]) + '\t' +
                        str(data[4]) + '\t' +
                        str(data[5]) + '\t')
    for ch in data[6]:
        spectresFile.write(str(ch) + ',')
    spectresFile.write('\n')
    i += 1

spectresFile.close()

print('done')