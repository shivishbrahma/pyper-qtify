import sys
from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QTextEdit)
from PyQt5.QtCore import Qt
import db
import markdown


class WordListItem(QListWidgetItem):
    def __init__(self, word, parent=None):
        super().__init__(word[1], parent)
        (id, name, pos, meaning, example) = word
        self.id = id
        self.name = name
        self.pos = pos
        self.meaning = meaning
        self.example = example


class DDApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Devil's Dictionary"
        self.left = 10
        self.top = 10
        self.width = 960
        self.height = 720

        self.database = db.DictDB("dict.db")
        self.initUI()
        self.wordList.setCurrentRow(0)

    def createWordTable(self, data):
        if data == None:
            return
        self.wordList.clear()
        c = 0
        for word in data:
            item = WordListItem(word, self.wordList)
            # self.wordList.addItem(item)
            c = c + 1

    def searchTextOnChange(self):
        searchTerm = self.searchText.text().strip()
        if searchTerm != "":
            self.createWordTable(self.database.searchWord(searchTerm))

    def onChangeSelected(self):
        item = self.wordList.currentItem()
        info = f'''
        {markdown.markdown(f'**{item.name}**')}
        {markdown.markdown(f'*{item.pos}*')}
        {markdown.markdown(item.meaning)}
        {markdown.markdown('**Examples**') if item.example.strip()!='' else ''}
        {markdown.markdown(f"{item.example}")}
        '''
        self.wordInfo.setHtml(info)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.searchText = QLineEdit()
        self.searchText.setPlaceholderText("Enter the search term...")
        self.searchText.setFixedWidth(400)
        self.searchText.textChanged.connect(self.searchTextOnChange)

        self.wordList = QListWidget()
        self.wordList.setMaximumWidth(270)
        self.createWordTable(self.database.searchWord())
        self.wordList.currentItemChanged.connect(self.onChangeSelected)

        self.wordInfo = QTextEdit()
        self.wordInfo.setFixedWidth(660)
        self.wordInfo.setReadOnly(True)

        layout = QVBoxLayout()

        row1 = QHBoxLayout()
        searchTermLabel = QLabel("Search term: ")
        searchTermLabel.setFixedWidth(300)
        row1.addWidget(searchTermLabel, 0, Qt.AlignRight)
        row1.addWidget(self.searchText, 0, Qt.AlignLeft)

        row2 = QHBoxLayout()
        row2.addWidget(self.wordList, 0, Qt.AlignLeft)
        row2.addWidget(self.wordInfo, 0, Qt.AlignRight)

        layout.addLayout(row1, 0)
        layout.addLayout(row2, 0)

        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dd = DDApp()
    if(app.exec_()):
        dd.database.closeDB()
        sys.exit()
