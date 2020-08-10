
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

        if self.debug:
            print(f"Row: {source_row}")
            print(f"Title: {title_str}")

        accept_child = False
        if self.sourceModel().hasChildren(title_index):
            num_children = self.sourceModel().rowCount(title_index)
            accept_child = any((self.filterAcceptsRow(child_row, title_index)) for child_row in range(num_children))

        if self.filter_type == "Contains":
            filter_fun = lambda x: self.filter_str in x
        elif self.filter_type == "Regular Expression":
            filter_fun = lambda x: self.filter_str in x
        elif self.filter_type == "Starts with":
            filter_fun = lambda x: x.startswith(self.filter_str)
        elif self.filter_type == "Ends with":
            filter_fun = lambda x: x.endswith(self.filter_str)
        else:
            raise ValueError(f"Unknown Filter syntax: {self.filter_type}")

        if self.filter_col == "Title" or self.filter_col == "Both":
            if title_str is None:
                raise ValueError(f"title_str is None")
            has_title = filter_fun(title_str) if self.filter_str else True

        if self.filter_col == "Summary" or self.filter_col == "Both":
            if summary_str is None:
                raise ValueError(f"summary_str is None")
            has_summary = filter_fun(summary_str) if self.filter_str else True

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
        self.filter_case_sensitive = state
        print(f"Case sensitive filter: {state}")
        self.invalidateFilter()

    @QtCore.pyqtSlot(int)
    def update_case_sensitive_sort(self, state):
        self.debug = True if state == 2 else False
        self.sorting_case_sensitive = state
        print(f"Case sensitive sort: {state}")
        # self.invalidateFilter()
