# Модуль, для обработки данных, записанных ПО Atom Spectra

from tkinter import filedialog
# import numpy as np
import datetime
import os

def atom_spectra_handling(file):
    # spectre_array = np.zeros(1024, np.uint32)
    file_spectre = open(file, 'r', encoding='ANSI')
    lines = file_spectre.readlines()

    # Calibratuin coeffitient kx+b, calculate in channels
    k = 0.32841
    b = 13.99
    # Каналы для расчета md283
    U1 = (211, 217)
    U2 = (349, 451)
    U3 = (604, 625)
    Th1 = (309, 332)
    Th2 = (805, 977)
    K = (464, 530)

    U_counts = 0
    Th_counts = 0
    K_counts = 0

    date_time = datetime.datetime.strptime((os.path.basename(file).split('.')[0]), '%Y%m%d_%H%M%S')
    posIsValid = 1
    expoTime = float(lines[4].split(' ')[9])
    counts = int(lines[5].split(' ')[7])
    cps = float(lines[6].split(' ')[5])

    spectre_string = ''
    counts = 0
    for i in range(13, 1036):
        chanel_count = int(lines[i].replace('\n', '').split('\t')[2])
        spectre_string = spectre_string + str(chanel_count)
        spectre_string = spectre_string + ';'

    spectre_record = (date_time.strftime("%d-%m-%YT%H:%M:%S"), cps, 0, 0, 88, 192, 662, 1460, expoTime, U_counts, Th_counts, K_counts, spectre_string)
    return spectre_record






spectre_files = filedialog.askopenfilenames(title=("Choose Spectre File"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
spectresFile = filedialog.asksaveasfile('w')
spectresFile.write('DATETIME\tCSP\tLAT\tLON\tch1Num\tch2Num\tch1En\tch2En\texpoTime\tU\tTh\tK\tspectre\n')

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