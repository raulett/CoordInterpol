from datetime import *
from tkinter import *
from tkinter import filedialog
import traceback

def getMagnData():
    filesMagn = filedialog.askopenfilenames(title = ("Choose Magnetic files"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
    val_points = []
    for file in filesMagn:
        fileRad = open(file, 'r')
        lines = fileRad.readlines()
        for line in lines:
            value = line.replace('\n', '').split(' ')
            if ((len(value))!=5):
                continue
            T = value[0]
            qmc = value[1]
            st = value[2]
            # try:
            # dateTime = datetime.strptime(value[3], "%d-%m-%yT%H:%M:%S,%f").timestamp()
            dateTime = datetime.strptime(value[3] + 'T' + value[4], "%m.%d.%yT%H:%M:%S,%f").timestamp()
            # except BaseException:
            #     try:
            #         dateTime = datetime.strptime(value[3] + 'T' + value[4], "%m-%d-%yT%H:%M:%S,%f").timestamp()
            #     except BaseException:
            #         traceback.print_exc()
            val_points.append((dateTime, (T, qmc, st)))
        fileRad.close()
    val_points = dict((x,y) for x, y in val_points)
    vals = []
    for key in val_points.keys():
        vals.append((key, val_points[key][0], val_points[key][1], val_points[key][2]))
    def getKey(item):
        return item[0]
    val_points = sorted(vals, key=getKey)
    return val_points

def getMagnDataGPS():
    filesMagn= filedialog.askopenfilenames(title=("Choose Magnetic files"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
    val_points = []
    for file in filesMagn:
        fileRad = open(file, 'r')
        lines = fileRad.readlines()
        for line in lines:
            value = line.replace('\n', '').split(' ')
            if ((len(value))!=5):
                continue
            T = value[0]
            qmc = value[1]
            st = value[2]
            # try:
            # dateTime = datetime.strptime(value[3], "%d-%m-%yT%H:%M:%S,%f").timestamp()
            dateTime = datetime.strptime(value[3] + 'T' + value[4], "%m.%d.%yT%H:%M:%S,%f").timestamp()
            # except BaseException:
            #     try:
            #         dateTime = datetime.strptime(value[3] + 'T' + value[4], "%m-%d-%yT%H:%M:%S,%f").timestamp()
            #     except BaseException:
            #         traceback.print_exc()
            val_points.append((dateTime, (T, qmc, st)))
        fileRad.close()
    val_points = dict((x,y) for x, y in val_points)
    vals = []
    for key in val_points.keys():
        vals.append((key, val_points[key][0], val_points[key][1], val_points[key][2]))
    def getKey(item):
        return item[0]
    val_points = sorted(vals, key=getKey)
    return val_points