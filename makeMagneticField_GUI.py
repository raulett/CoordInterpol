# Связывает файлы магнитометра с данными координат из GPX
# Сдвиг времени (часовой пояс) задается в файле transformCoord.openGpxFiles
from PyQt5 import QtWidgets
import sys
from UI.BindMagnFile_handle import BindMagnFile_handle

app = QtWidgets.QApplication([])
window = BindMagnFile_handle()
window.show()

sys.exit(app.exec())