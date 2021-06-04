# Берет файлы ASW и компанует их в один TAB separated text и расчитывает каналы U, Th, K, на основе данных из блока констант ниже.

from tkinter import filedialog
import numpy as np

def getASWdataFromFile(file):
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

    spectre_array = np.zeros(1024, np.uint32)
    fileASW = open(file, 'r', encoding='ANSI')
    lines = fileASW.readlines()
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
    spectreByte = binData[index+9:len(binData)-1]
    spectreInt = []
    counter = 0

    U_counts = 0
    Th_counts = 0
    K_counts = 0

    for b in range(0, len(spectreByte)//4):
        # int_val = b'\\{}\\{}\\{}\\{}'.format((spectreByte[b*4] << 24), (spectreByte[b*4 + 1]<< 16), (spectreByte[b*4 + 2] << 8), (spectreByte[b*4 + 3]))
        intVal = ((spectreByte[b*4]) + (spectreByte[b*4 + 1]<< 8) + (spectreByte[b*4 + 2] << 16) + (spectreByte[b*4 + 3] << 24))
        spectreInt.append(intVal)
        spectre_array[counter] = intVal
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

    spectreRec = (lines[DateIndex+2].replace('\n', '').replace('Spectrum=', '')  + 'T' + lines[TimeIndex+2].replace('\n', '').replace('Spectrum=', ''),
                  lines[PosIndex+1].replace('\n', '').replace('IsValid=', ''), lines[PosIndex+2].replace('\n', '').replace('Latitude=', ''), lines[PosIndex+3].replace('\n', '').replace('Longitude=', ''),
                  lines[EnCalibrationIndex+2].replace('\n', '').replace('Channel1=', ''), lines[EnCalibrationIndex+3].replace('\n', '').replace('Channel2=', ''),
                 lines[EnCalibrationIndex+5].replace('\n', '').replace('Energy1=', ''), lines[EnCalibrationIndex+6].replace('\n', '').replace('Energy2=', ''),
                  lines[epositionTimeIndex+3].replace('\n', '').replace('Real=', ''), str(U_counts), str(Th_counts), str(K_counts), str(spectreInt).replace('[', '').replace(']', '').replace(',', ';'))

    fileASW.close()
    return spectreRec

filesASW = filedialog.askopenfilenames(title=("Choose Spectre File"),
                                       filetypes=(("Template files", "*.asw"), ("All files", "*.*")))
spectresFile = filedialog.asksaveasfile('w')
spectresFile.write('DATETIME\tPosIsValid\tLAT\tLON\tch1Num\tch2Num\tch1En\tch2En\texpoTime\tU\tTh\tK\tspectre\n')

for file in filesASW:
    try:
        aswRecord = getASWdataFromFile(file)
        spectresFile.write(aswRecord[0] + '\t' + aswRecord[1] + '\t' + format(float(aswRecord[2]), '.6f') + '\t' + format(float(aswRecord[3]), '.6f') + '\t' + aswRecord[4] + '\t' +
                            aswRecord[5] + '\t' + aswRecord[6] + '\t' + aswRecord[7] + '\t' + aswRecord[8] + '\t' + aswRecord[9] + '\t' + aswRecord[10] + '\t' + aswRecord[11] + '\t' + aswRecord[12] + '\n')
    except UnicodeDecodeError:
        continue

spectresFile.close()


