from PyQt5 import QtWidgets


class WordListItem(QtWidgets.QListWidgetItem):
    def __init__(self, word, parent=None):
        super().__init__(word[1], parent)
        (id, name, pos, meaning, example) = word
        self.id = id
        self.name = name
        self.pos = pos
        self.meaning = meaning
        self.example = example
