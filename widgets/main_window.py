
from PyQt5 import QtCore, QtWidgets

from .main_window_base import Ui_MainWindow
from .custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from .tree_model import TreeModel

model_filename = "widgets/default.txt"


class MainWindow(Ui_MainWindow, QtCore.QObject):

    def __init__(self, qmain_window):
        super().__init__()
        self.setupUi(qmain_window)

        self._proxy_model = CustomSortFilterProxyModel(self)
        self._model = TreeModel(model_filename)
        self._proxy_model.setSourceModel(self._model)
        self.treeView.setModel(self._proxy_model)

        self.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
