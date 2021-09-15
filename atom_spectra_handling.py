# Модуль, для обработки данных, записанных ПО Atom Spectra

from tkinter import filedialog
import numpy as np
import datetime
import os

def atom_spectra_handling(file):
    # spectre_array = np.zeros(1024, np.uint32)
    file_spectre = open(file, 'r', encoding='ANSI')
    lines = file_spectre.readlines()

    # Calibration coefficient kx+b, calculate in channels
    k = 0.3388
    b = 15.649
    # Каналы для расчета md283
    U1 = (int(k*604+b), int(k*619+b))
    U2 = (int(k*1020+b), int(k*1330+b))
    U3 = (int(k*1660+b), int(k*1860+b))
    Th1 = (int(k*900+b), int(k*970+b))
    Th2 = (int(k*2410+b), int(k*2810+b))
    K = (int(k*1370+b), int(k*1570+b))
    integral = (int(k*400+b), int(k*2810+b))

    spectre_array = np.zeros(1024, np.uint32)

    U_counts = 0
    Th_counts = 0
    K_counts = 0

    date_time = datetime.datetime.strptime((os.path.basename(file).split('.')[0]), '%Y%m%d_%H%M%S')
    posIsValid = 1
    expoTime = float(lines[4].split(' ')[9])
    counts = int(lines[5].split(' ')[7])
    cps = float(lines[6].split(' ')[5])

    spectre_string = ''
    counter = 0
    for i in range(13, 1036):
        chanel_count = int(lines[i].replace('\n', '').split('\t')[2])
        spectre_string = spectre_string + str(chanel_count)
        spectre_string = spectre_string + ';'

        spectre_array[counter] = chanel_count
        counter += 1

    for i in range(U1[0], U1[1]+1):
        U_counts += spectre_array[i]

    for i in range(U2[0], U2[1]+1):
        U_counts += spectre_array[i]

    for i in range(U3[0], U3[1]+1):
        U_counts += spectre_array[i]

    for i in range(Th1[0], Th1[1]+1):
        Th_counts += spectre_array[i]

    for i in range(Th2[0], Th2[1]+1):
        Th_counts += spectre_array[i]

    for i in range(K[0], K[1]+1):
        K_counts += spectre_array[i]

    counts = 0
    for i in range(integral[0], integral[1]+1):
        counts += spectre_array[i]

    spectre_record = (date_time.strftime("%d-%m-%YT%H:%M:%S"), counts, 0, 0, 88, 192, 662, 1460, expoTime, U_counts, Th_counts, K_counts, spectre_string)
    return spectre_record






spectre_files = filedialog.askopenfilenames(title=("Choose Spectre File"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
spectresFile = filedialog.asksaveasfile('w')
spectresFile.write('DATETIME\tcounts\tLAT\tLON\tch1Num\tch2Num\tch1En\tch2En\texpoTime\tU\tTh\tK\tspectre\n')

for file in spectre_files:
    try:
        spectre_record = atom_spectra_handling(file)
        spectresFile.write(spectre_record[0] + '\t' + str(spectre_record[1]) + '\t' +
                           format(float(spectre_record[2]), '.6f') + '\t' + format(float(spectre_record[3]), '.6f') +
                           '\t' + format(float(spectre_record[4]), '.2f') + '\t' + str(spectre_record[5]) + '\t' +
                           str(spectre_record[6]) + '\t' +  str(spectre_record[7]) + '\t' +
                           str(spectre_record[8]) + '\t' +  str(spectre_record[9]) + '\t' +
                           str(spectre_record[10]) + '\t' +  str(spectre_record[11]) + '\t' +
                           spectre_record[12] + '\n')
    except UnicodeDecodeError:
        continue