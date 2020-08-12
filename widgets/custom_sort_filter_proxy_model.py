
import re

from PyQt5 import QtCore, QtGui, QtWidgets


class CustomSortFilterProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_str = None
        self.filter_type = "Contains"
        self.filter_col = "Both"
        self.filter_case_sensitive = False
        self.sorting_case_sensitive = False

        self.debug = False

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        has_title = False
        has_summary = False

        title_index = self.sourceModel().index(source_row, 0, source_parent)
        summary_index = self.sourceModel().index(source_row, 1, source_parent)

        title_str = self.sourceModel().data(title_index, role=QtCore.Qt.DisplayRole).value()
        summary_str = self.sourceModel().data(summary_index, role=QtCore.Qt.DisplayRole).value()

        accept_child = False
        if self.sourceModel().hasChildren(title_index):
            num_children = self.sourceModel().rowCount(title_index)
            accept_child = any((self.filterAcceptsRow(child_row, title_index)) for child_row in range(num_children))

        filter_str = self.filter_str

        if not self.filter_case_sensitive:
            if self.filter_str:
                filter_str = filter_str.lower()
            if title_str:
                title_str = title_str.lower()
            if summary_str:
                summary_str = summary_str.lower()

        if self.filter_type == "Contains":
            filter_fun = lambda x: filter_str in x
        elif self.filter_type == "Regular Expression":
            flags = 0 if self.filter_case_sensitive else re.IGNORECASE
            try:
                pattern = re.compile(filter_str, flags=flags)
                filter_fun = lambda x: bool(pattern.search(x))
            except TypeError:  #  Invalid patterns will default to searching for everything.
                filter_fun = pattern = re.compile(".*")
        elif self.filter_type == "Starts with":
            filter_fun = lambda x: x.startswith(filter_str)
        elif self.filter_type == "Ends with":
            filter_fun = lambda x: x.endswith(filter_str)
        else:
            raise ValueError(f"Unknown Filter syntax: {self.filter_type}")

        if self.filter_col == "Title" or self.filter_col == "Both":
            has_title = filter_fun(title_str) if self.filter_str else True

        if self.filter_col == "Summary" or self.filter_col == "Both":
            has_summary = filter_fun(summary_str) if self.filter_str else True

        if self.debug:
            print(f"Title: {title_str}")

        return has_title or has_summary or accept_child

    @QtCore.pyqtSlot(str)
    def update_filter_pattern(self, filter_pattern):
        self.filter_str = filter_pattern
        self.invalidateFilter()

    @QtCore.pyqtSlot(str)
    def update_filter_syntax(self, filter_syntax):
        print(f"Filter type: {filter_syntax}")
        self.filter_type = filter_syntax
        self.invalidateFilter()

    @QtCore.pyqtSlot(str)
    def update_filter_column(self, filter_column):
        self.filter_col = filter_column
        self.invalidateFilter()

    @QtCore.pyqtSlot(int)
    def update_case_sensitive_filter(self, state):
        self.filter_case_sensitive = state == 2
        self.invalidateFilter()

    @QtCore.pyqtSlot(int)
    def update_case_sensitive_sort(self, state):
        self.debug = state == 2
        self.sorting_case_sensitive = state
        print(f"Case sensitive sort: {state}")
        # self.invalidateFilter()
