from datetime import *
from tkinter import *
from tkinter import filedialog


def getRadData():

    filesRad = filedialog.askopenfilenames(title = ("Choose radiation files"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
    val_points = []
    for file in filesRad:
        fileRad = open(file, 'r')
        lines = fileRad.readlines()
        for line in lines:
            value = line.replace('\n', '').split('\t')
            val_points.append(((datetime.strptime(value[1], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=0)).timestamp(), value[0]))
        fileRad.close()
    val_points = dict((x,y) for x, y in val_points)
    vals = []
    for key in val_points.keys():
        vals.append((key, val_points[key]))
    def getKey(item):
        return item[0]
    val_points = sorted(vals, key=getKey)
    return val_points