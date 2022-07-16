# Берет файлы *.dat из спектрометра shproto и компанует их в один TAB separated text и расчитывает каналы U, Th, K, на основе данных из блока констант ниже.

from tkinter import filedialog
import numpy as np
import os
import datetime
from GetSpatialData import openGpxFiles
import coordFunction

timeshift = 0

def get_data_from_CSV(filename):

    # Calibration coefficient kx+b, calculate in channels
    #Calibration kb_radar_4096_01
    k = 2.73958333
    b = 25.66666667


    # u0_1_2_609KEv = (int(k*609+b), int(k*650+b))
    # u1_2205KEv = (int(k * 2145 + b), int(k * 2265 + b))
    # u2_1120KEv  = (int(k*1020+b), int(k*1330+b))
    # u3_1760KEv = (int(k*1660+b), int(k*1860+b))
    # th1_910KEv = (int(k*900+b), int(k*970+b))
    # th2_2620KEv = (int(k*2410+b), int(k*2810+b))
    # K = (int(k*1370+b), int(k*1570+b))
    # integral = (int(k*400+b), int(k*2810+b))

    u0_1_2_609KEv = (int(k * 607 + b), int(k * 664 + b)) #609 1/2 пика
    u1_2205KEv = (int(k * 2025 + b), int(k * 2300 + b)) #корректировка по графику 2.2
    u2_1120KEv = (int(k*1050+b), int(k*1305+b)) #1120/ 2пика 7 и 8
    u3_1760KEv = (int(k*1670+b), int(k*1835+b)) #1,76
    th1_910KEv = (int(k*870+b), int(k*1010+b)) #910
    th2_2620KEv = (int(k*2510+b), int(k*2670+b)) #2.4 переделать 2.62
    K = (int(k*1340+b), int(k*1535+b)) #1459 K40
    integral = (int(k*400+b), int(k*2810+b))

    spectrum_len = 8192

    spectreRecords = []
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        line = line.replace('\n', '').split('\t')
        # date_time = datetime.datetime.strptime(line[0], '%d-%m-%YT%H:%M:%S')
        date_time = line[0]
        try:
            lon = float(line[1])
            lat = float(line[2])
            alt = float(line[3])
        except ValueError:
            print(ValueError)
            continue

        spectre_array = np.zeros(spectrum_len, np.uint32)
        spectrum_rec = line[9].split(',')
        try:
            for i in range(spectrum_len):
                try:
                    spectre_array[i] = int(spectrum_rec[i])
                except:
                    print("Int parse error {}".format(spectrum_rec[i]))

        except IndexError:
            print(filename)
            print(line)
            return 1


        U0_1_2_609KEv_counts = 0
        u1_2205KEv_counts = 0
        u2_1175KEv_counts = 0
        u3_1760KEv_counts = 0
        th1_935KEv_counts = 0
        th2_2610KEv_counts = 0
        K_counts = 0
        int_counts = 0

        for i in range(u0_1_2_609KEv[0], u0_1_2_609KEv[1] + 1):
            U0_1_2_609KEv_counts += spectre_array[i]

        for i in range(u1_2205KEv[0], u1_2205KEv[1] + 1):
            u1_2205KEv_counts += spectre_array[i]

        for i in range(u2_1120KEv[0], u2_1120KEv[1] + 1):
            u2_1175KEv_counts += spectre_array[i]

        for i in range(u3_1760KEv[0], u3_1760KEv[1] + 1):
            u3_1760KEv_counts += spectre_array[i]


        for i in range(th1_910KEv[0], th1_910KEv[1] + 1):
            th1_935KEv_counts += spectre_array[i]

        for i in range(th2_2620KEv[0], th2_2620KEv[1] + 1):
            th2_2610KEv_counts += spectre_array[i]


        for i in range(K[0], K[1] + 1):
            K_counts += spectre_array[i]

        for i in range(integral[0], integral[1] + 1):
            int_counts += spectre_array[i]

        spectreRecords.append((date_time, lon, lat, alt, int_counts, U0_1_2_609KEv_counts, u1_2205KEv_counts, u2_1175KEv_counts, u3_1760KEv_counts, th1_935KEv_counts, th2_2610KEv_counts, K_counts, line[9]))
    return spectreRecords








fileDAT = filedialog.askopenfilename(title=("Choose Spectre files"),
                                       filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
spectresFile = filedialog.asksaveasfile('w')


spectresFile.write('DATETIME\tLON\tLAT\tALT\tINT\tU_1/2_609\tu1_2205KEv\tu2_1120KEv\tu3_1760KEv\tth1_910KEv\tth2_2610KEv\tK\tspectre\n')


data = get_data_from_CSV(fileDAT)
for data_rec in data:
    spectresFile.write(data_rec[0] + '\t' +
                        str(data_rec[1]) + '\t' +
                        str(data_rec[2]) + '\t' +
                        str(data_rec[3]) + '\t' +
                        str(data_rec[4]) + '\t' +
                        str(data_rec[5]) + '\t' +
                        str(data_rec[6]) + '\t' +
                        str(data_rec[7]) + '\t' +
                        str(data_rec[8]) + '\t' +
                        str(data_rec[9]) + '\t' +
                        str(data_rec[10]) + '\t' +
                        str(data_rec[11]) + '\t' +
                        str(data_rec[12]) + '\n')


spectresFile.close()

print('done')