

import sys
from PyQt5 import QtWidgets

from widgets import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qmainWindow = QtWidgets.QMainWindow()
    uiMainWin = MainWindow(qmainWindow)
    qmainWindow.show()
    sys.exit(app.exec_())
