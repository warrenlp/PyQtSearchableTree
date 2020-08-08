
from PyQt5 import QtCore

from .main_window_base import Ui_MainWindow
from .tree_model import TreeModel

model_filename = "widgets/default.txt"


class MainWindow(Ui_MainWindow, QtCore.QObject):

    def __init__(self, qmainWindow):
        super().__init__()
        self.setupUi(qmainWindow)

        self._model = TreeModel(model_filename)
        self.treeView.setModel(self._model)
