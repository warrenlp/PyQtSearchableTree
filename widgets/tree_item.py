
class TreeItem(object):

    def __init__(self, data, parent=None):
        self.__child_items = []
        self.__item_data = data
        self.__parent = parent

    @property
    def parent(self):
        return self.__parent

    def append_child(self, child):
        self.__child_items.append(child)

    def child(self, row):
        if row < 0 or row >= len(self.__child_items):
            return None
        return self.__child_items[row]

    def child_count(self):
        return len(self.__child_items)

    def row(self):
        if self.__parent is not None:
            return self.__parent.__child_items.index(self)

        return 0

    def column_count(self):
        return len(self.__item_data)

    def data(self, column):
        if column < 0 or column >= len(self.__item_data):
            return
        return self.__item_data[column]
