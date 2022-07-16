 # Берет файлы ASW и компанует их в один TAB separated text и расчитывает каналы U, Th, K, на основе данных из блока констант ниже.

from tkinter import filedialog
import numpy as np
import pathlib
import datetime

time_delta = 0
# time_delta = -2


def getASWdataFromFile(file):
    # Calibration coefficient kx+b, calculate in channels
    k = 0.3388
    b = 15.649
    # Каналы для расчета md283
    U1 = (int(k * 609 + b), int(k * 619 + b))  # 1/2 609KEv
    U1_1 = (int(k * 612 + b), int(k * 619 + b))  # 1/3 609KEv
    U2 = (int(k * 1020 + b), int(k * 1330 + b))  # 1.12MEv
    U2_1 = (int(k * 1120 + b), int(k * 1250 + b))  # 1/2 1.12MEv
    U3 = (int(k * 1660 + b), int(k * 1860 + b))  # 1.76MEv
    U5 = (int(k * 2050 + b), int(k * 2350 + b))  # 2.2MEv
    Th1 = (int(k * 900 + b), int(k * 970 + b))
    Th2 = (int(k * 2410 + b), int(k * 2810 + b))  # 2.6MEv
    K = (int(k * 1370 + b), int(k * 1570 + b))
    integral = (int(k * 400 + b), int(k * 2810 + b))

    spectre_array = np.zeros(1024, np.uint32)
    fileASW = open(file, 'r', encoding='ANSI')
    lines = fileASW.readlines()
    # print(lines)
    spectreRecords = []
    linesLen = len(lines)
    print(file)
    PosIndex = lines.index("[GeoPosition]\n")
    DateIndex = lines.index("[Date]\n")
    TimeIndex = lines.index("[Time]\n")
    EnCalibrationIndex = lines.index("[Energy_calibration]\n")
    epositionTimeIndex = lines.index("[Exposition]\n")
    SpectreIndex = lines.index("[BEGIN]\n")
    # Date, Time, isValidPos, LAT, LON, ExpositionTime, calibratioCh1, calibratioCh2, calibratioEn1, calibratioEn2, spectre
    fileASW.close()
    fileASW = open(file, 'rb')
    binData = fileASW.read()
    index = binData.find('[BEGIN]\r\n'.encode("UTF-8"))
    spectreByte = binData[index + 9:len(binData) - 1]
    spectreInt = []
    counter = 0

    U1_counts = 0
    U2_counts = 0
    U3_counts = 0
    U4_counts = 0
    Th_counts = 0
    K_counts = 0
    integral_counts = 0

    for b in range(0, len(spectreByte) // 4):
        # int_val = b'\\{}\\{}\\{}\\{}'.format((spectreByte[b*4] << 24), (spectreByte[b*4 + 1]<< 16), (spectreByte[b*4 + 2] << 8), (spectreByte[b*4 + 3]))
        intVal = ((spectreByte[b * 4]) + (spectreByte[b * 4 + 1] << 8) + (spectreByte[b * 4 + 2] << 16) + (
                spectreByte[b * 4 + 3] << 24))
        spectreInt.append(intVal)
        spectre_array[counter] = intVal
        counter += 1

    # calculate U1 channel (1/2*609 + 1.12+ 1.76)
    # 1/2 609KEv
    for i in range(U1[0], U1[1] + 1):
        U1_counts += spectre_array[i]

    # 1.12MEv
    for i in range(U2[0], U2[1] + 1):
        U1_counts += spectre_array[i]

    # 1.76MEv
    for i in range(U3[0], U3[1] + 1):
        U1_counts += spectre_array[i]

    # calculate U2 channel (1.12+1.76+2.2)
    # 1.12MEv
    for i in range(U2[0], U2[1] + 1):
        U2_counts += spectre_array[i]

    # 1.76MEv
    for i in range(U3[0], U3[1] + 1):
        U2_counts += spectre_array[i]

    # 2.2MEv
    for i in range(U5[0], U5[1] + 1):
        U2_counts += spectre_array[i]

    # calculate U3 channel (1/3*609 + 1.12 + 2.2 + 2.6)
    # 1/3 609KEv
    for i in range(U1_1[0], U1_1[1] + 1):
        U3_counts += spectre_array[i]

    # 1.12MEv
    for i in range(U2[0], U2[1] + 1):
        U3_counts += spectre_array[i]

    # 2.2MEv
    for i in range(U5[0], U5[1] + 1):
        U3_counts += spectre_array[i]

    # 1.76MEv
    for i in range(U3[0], U3[1] + 1):
        U3_counts += spectre_array[i]

    #Th
    for i in range(Th1[0], Th1[1] + 1):
        Th_counts += spectre_array[i]

    for i in range(Th2[0], Th2[1] + 1):
        Th_counts += spectre_array[i]

    # K
    for i in range(K[0], K[1] + 1):
        K_counts += spectre_array[i]

#int
    for i in range(integral[0], integral[1] + 1):
        integral_counts += spectre_array[i]

    #U4
    # 1/2 609KEv
    for i in range(U1[0], U1[1] + 1):
        U4_counts += spectre_array[i]

    # 1.12MEv
    for i in range(U2_1[0], U2_1[1] + 1):
        U4_counts += spectre_array[i]

    # 1.76MEv
    for i in range(U3[0], U3[1] + 1):
        U4_counts += spectre_array[i]

    time = datetime.datetime(2000, 1, 1)
    try:
        time = datetime.datetime.strptime(lines[DateIndex + 2].replace('\n', '').replace('Spectrum=', '')
                                          + 'T' + lines[TimeIndex + 2].replace('\n', '').replace('Spectrum=', ''),
                                          '%d.%m.%YT%H:%M:%S') + datetime.timedelta(seconds=time_delta)
    except ValueError:
        try:
            time = datetime.datetime.strptime(lines[DateIndex + 2].replace('\n', '').replace('Spectrum=', '')
                                              + 'T' + lines[TimeIndex + 2].replace('\n', '').replace('Spectrum=', ''),
                                              '%d.%m.%YT%-H:%M:%S') + datetime.timedelta(seconds=time_delta)
        except ValueError:
            print(ValueError)
            print(lines[DateIndex + 2].replace('\n', '').replace('Spectrum=', '') + 'T'
                  + lines[TimeIndex + 2].replace('\n', '').replace('Spectrum=', ''))

    spectre_rec = (
        time.strftime('%d.%m.%YT%H:%M:%S'),  # 0
        lines[PosIndex + 1].replace('\n', '').replace('IsValid=', ''),  # 1
        lines[PosIndex + 2].replace('\n', '').replace('Latitude=', ''),  # 2
        lines[PosIndex + 3].replace('\n', '').replace('Longitude=', ''),  # 3
        lines[EnCalibrationIndex + 2].replace('\n', '').replace('Channel1=', ''),  # 4
        lines[EnCalibrationIndex + 3].replace('\n', '').replace('Channel2=', ''),  # 5
        lines[EnCalibrationIndex + 5].replace('\n', '').replace('Energy1=', ''),  # 6
        lines[EnCalibrationIndex + 6].replace('\n', '').replace('Energy2=', ''),  # 7
        lines[epositionTimeIndex + 3].replace('\n', '').replace('Real=', ''),  # 8
        str(integral_counts),  # 9
        str(U1_counts),  # 10
        str(U2_counts),  # 11
        str(U3_counts),  # 12
        str(U4_counts),  # 13
        str(Th_counts),  # 14
        str(K_counts),  # 15
        str(spectreInt).replace('[', '').replace(']', '').replace(',', ';'))  # 16

    fileASW.close()
    return spectre_rec


folder = filedialog.askdirectory()
filepattern = r"**\*.asw"
filesASW = list(pathlib.Path(folder).glob(filepattern))
# filesASW = filedialog.askopenfilenames(title=("Choose Spectre File"),
#                                        filetypes=(("Template files", "*.asw"), ("All files", "*.*")))
spectresFile = filedialog.asksaveasfile(title="save spectrum file", mode='w')
spectresFile.write('DATETIME\tPosIsValid\tLAT\tLON\tch1Num\tch2Num\tch1En\tch2En\texpoTime'
                   '\tint\tU1\tU2\tU3\tU4\tTh\tK\tspectre\n')

counter = 0
files_count = len(filesASW)

for file in filesASW:
    counter += 1
    print('handele {} file of {}; '.format(counter, files_count), end='\n')
    # try:
    aswRecord = getASWdataFromFile(file)
    spectresFile.write(aswRecord[0] + '\t' + aswRecord[1]
                       + '\t' + format(float(aswRecord[2]), '.6f') + '\t' + format(float(aswRecord[3]), '.6f')
                       + '\t' + aswRecord[4] + '\t' + aswRecord[5] + '\t' + aswRecord[6]
                       + '\t' + aswRecord[7] + '\t' + aswRecord[8]
                       + '\t' + aswRecord[9] + '\t' + aswRecord[10] + '\t' + aswRecord[11] + '\t' + aswRecord[12]
                       + '\t' + aswRecord[13] + '\t' + aswRecord[14] + '\t' + aswRecord[15] + '\t' + aswRecord[
                           16] + '\n')
    # except UnicodeDecodeError:
    #     print(UnicodeDecodeError)
    #     continue
    # except ValueError:
    #     print(ValueError)
    #     continue
spectresFile.close()
