
from PyQt5 import QtCore, Qt

from .tree_item import TreeItem


class TreeModel(QtCore.QAbstractItemModel):

    def __init__(self, setup_filename, parent=None):
        super().__init__(parent)

        self._root_item = TreeItem(["Title", "Summary"])
        self._setup_model_data(setup_filename)

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        if child_item := parent_item.child(row):
            return self.createIndex(row, column, child_item)

        return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent

        if parent_item == self._root_item:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().column_count()

        return self._root_item.column_count()

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return super().flags(index)

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._root_item.data(section)

        return QtCore.QVariant()

    def _setup_model_data(self, filename):
        with open(filename, "r") as infile:
            lines = infile.read().splitlines()

        parents = [self._root_item]
        indentations = [0]

        for line in lines:
            line_data = line.strip()
            if not line_data:
                continue

            for position, char in enumerate(line):
                if char != " ":
                    break

            column_data = [QtCore.QVariant(col_str) for col_str in line_data.split("\t") if col_str]

            if position > indentations[-1]:
                # The last child of the current parent is now the new parent
                # unless the current parent has no children.
                if parents[-1].child_count() > 0:
                    parents.append(parents[-1].child(parents[-1].child_count()-1))
                    indentations.append(position)
            else:
                while position < indentations[-1] and len(parents) > 0:
                    parents.pop()
                    indentations.pop()

            # Append a new item to the current parent's list of children
            parents[-1].append_child(TreeItem(column_data, parents[-1]))
