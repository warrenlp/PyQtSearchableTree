
from PyQt5 import QtCore, QtGui, QtWidgets


class CustomSortFilterProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_str = None
        self.filter_type = None
        self.filter_col = None

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        title_index = self.sourceModel().index(source_row, 0, source_parent)
        summary_index = self.sourceModel().index(source_row, 0, source_parent)

        title_str = self.sourceModel().data(title_index, role=QtCore.Qt.DisplayRole).value()
        summary_str = self.sourceModel().data(summary_index, role=QtCore.Qt.DisplayRole).value()

        has_title = self.filter_str in title_str if self.filter_str else True
        has_summary = self.filter_str in summary_str if self.filter_str else True

        return has_title or has_summary
