import glob
from tkinter import filedialog
import pathlib

folder = filedialog.askdirectory()
filepattern = r"**\*.asw"


files = list(pathlib.Path(folder).glob(filepattern))
print(files)
