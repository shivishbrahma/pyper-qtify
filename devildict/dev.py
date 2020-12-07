import sys

from PyQt5.QtWidgets import (QApplication, QAbstractItemView, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMessageBox, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QHeaderView)
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5 import QtCore
import db


class AddWordForm(QDialog):

    def __init__(self, parent=None):
        super(AddWordForm, self).__init__(parent)
        self.posList = ["Noun(n.)", "Adjective(adj.)", "Verb(v.)",
                        "Verb Transitive(v.t.)", "Verb Intransitive(v.i.)", "Adverb(adv.)",
                        "Past Participle(pp.)", "Preposition(prep.)", "Pronoun(pron.)",
                        "Exclamation(exclam.)"]
        self.posList.sort()
        self.createAddWordForm()

        self.title = "Add Word Form - Devil's Dictionary"
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 600

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.initUI()

    def createAddWordForm(self):
        self.formGroupBox = QGroupBox("Add Word")
        self.nameText = QLineEdit()

        self.posCombo = QComboBox()
        for pos in self.posList:
            self.posCombo.addItem(pos)

        self.meanText = QTextEdit()
        self.exText = QTextEdit()
        layout = QFormLayout()
        layout.addRow(QLabel("Name: "), self.nameText)
        layout.addRow(QLabel("POS: "), self.posCombo)
        layout.addRow(QLabel("Meaning: "), self.meanText)
        layout.addRow(QLabel("Example: "), self.exText)
        self.formGroupBox.setLayout(layout)

    def initUI(self):
        if self.parent() is not None:
            self.left = self.parent().left
            self.top = self.parent().top
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def getWordData(self):
        name = self.nameText.text().strip()
        pos = self.posCombo.currentText().strip()
        meaning = self.meanText.toPlainText().strip()
        example = self.exText.toPlainText().strip()
        return (name, pos, meaning, example)

    def setWordData(self, name: str, pos: str, meaning: str, example: str):
        self.nameText.setText(name.strip())
        self.posCombo.setCurrentText(pos.strip())
        self.meanText.setText(meaning.strip())
        self.exText.setText(example.strip())

    def clear(self):
        self.nameText.setText("")
        self.posCombo.setCurrentIndex(0)
        self.meanText.setText("")
        self.exText.setText("")


class FindWordForm(QDialog):
    def __init__(self, parent=None):
        super(FindWordForm, self).__init__(parent)
        self.createFindWordForm()

        self.title = "Find Word Form - Devil's Dictionary"
        self.left = 10
        self.top = 10
        self.width = 520
        self.height = 240

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.initUI()

    def createFindWordForm(self):
        self.formGroupBox = QGroupBox("Find Word")
        self.searchText = QLineEdit()

        layout = QFormLayout()
        layout.addRow(QLabel("Search term"))
        layout.addRow(self.searchText)

        self.formGroupBox.setLayout(layout)

    def getSearchTerm(self):
        return self.searchText.text()

    def clear(self):
        self.searchText.setText("")

    def initUI(self):
        if self.parent() is not None:
            self.left = self.parent().left
            self.top = self.parent().top
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


class ViewWidget(QDialog):
    def __init__(self, parent=None):
        super(ViewWidget, self).__init__(parent)
        self.createViewWordForm()

        self.title = "View Word - Devil's Dictionary"
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 600

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.accept)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.initUI()

    def createViewWordForm(self):
        self.formGroupBox = QGroupBox("View Word")
        self.nameLabel = QLabel()
        self.posLabel = QLabel()
        self.meanLabel = QTextEdit()
        self.meanLabel.setEnabled(False)
        self.exLabel = QTextEdit()
        self.exLabel.setEnabled(False)
        layout = QFormLayout()
        layout.addRow(QLabel("Name: "), self.nameLabel)
        layout.addRow(QLabel("POS: "), self.posLabel)
        layout.addRow(QLabel("Meaning: "), self.meanLabel)
        layout.addRow(QLabel("Example: "), self.exLabel)
        self.formGroupBox.setLayout(layout)

    def setWordData(self, name: str, pos: str, meaning: str, example: str):
        # print(name, pos, meaning, example)
        self.nameLabel.setText(name.strip())
        self.posLabel.setText(pos.strip())
        self.meanLabel.setMarkdown(meaning.strip())
        self.exLabel.setMarkdown(example.strip())

    def initUI(self):
        if self.parent() is not None:
            self.left = self.parent().left
            self.top = self.parent().top
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


class DDApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Devil's Dictionary"
        self.left = 10
        self.top = 10
        self.width = 960
        self.height = 720

        self.database = db.DictDB("dict.db")
        self.awfDialog = AddWordForm(self)
        self.fwfDialog = FindWordForm(self)
        self.vwfDialog = ViewWidget(self)
        self.initUI()
        self.dataTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dataTable.customContextMenuRequested.connect(self.rightClickMenu)

    def initAddWord(self):
        self.awfDialog.setWindowTitle("Add Word - Devil's Dictionary")
        self.awfDialog.formGroupBox.setTitle("Add Word")
        self.awfDialog.clear()
        self.awfDialog.show()
        if self.awfDialog.exec_():
            (name, pos, meaning, example) = self.awfDialog.getWordData()
            if name != "" or pos != "" or meaning != "":
                self.database.insertWord(name, pos, meaning, example)
                self.createWordTable(self.database.searchWord())
                QMessageBox.about(self, "Add Word",
                                  "Added new word successfully!")

    def initEditWord(self):
        if self.dataTable.currentRow() < 0:
            QMessageBox.warning(self, "Edit Word", "Please select a word!")
            return
        r, c = self.dataTable.currentRow(), self.dataTable.currentColumn()
        id = self.dataTable.item(r, 4).text()
        row = self.database.getOneWord("id", id)
        if row != None:
            (id, name, pos, meaning, example) = self.database.getOneWord("id", id)
        else:
            QMessageBox.about(self, "Edit Word",
                              "Database cannot find the entry!")
            return

        self.awfDialog.setWindowTitle("Edit Word - Devil's Dictionary")
        self.awfDialog.formGroupBox.setTitle("Edit Word")
        self.awfDialog.setWordData(name, pos, meaning, example)
        self.awfDialog.show()
        if self.awfDialog.exec_():
            with_value = self.awfDialog.getWordData()
            with_prop = ("name", "pos", "mean", "ex")
            self.database.updateWord(with_prop, with_value, "id", id)
            self.createWordTable(self.database.searchWord())
            self.dataTable.setCurrentCell(r, c)
            QMessageBox.about(self, "Edit Word",
                              "Updated word successfully!")

    def initViewWord(self):
        if self.dataTable.currentRow() < 0:
            QMessageBox.warning(self, "View Word", "Please select a word!")
            return
        r, c = self.dataTable.currentRow(), self.dataTable.currentColumn()
        id = self.dataTable.item(r, 4).text()
        row = self.database.getOneWord("id", id)
        if row != None:
            (id, name, pos, meaning, example) = self.database.getOneWord("id", id)
        else:
            QMessageBox.about(self, "View Word",
                              "Database cannot find the entry!")
            return

        self.vwfDialog.setWordData(name, pos, meaning, example)
        self.vwfDialog.show()

    def initDeleteWord(self):
        if self.dataTable.currentRow() < 0:
            QMessageBox.warning(self, "Delete Word", "Please select a word!")
            return

        currentRow = self.dataTable.currentRow()
        name = self.dataTable.item(currentRow, 0).text()
        row = self.database.getOneWord("id", id)
        if row != None:
            (id, name, pos, meaning, example) = self.database.getOneWord("id", id)
        else:
            QMessageBox.about(self, "Delete Word",
                              "Database cannot find the entry!")
            return

        ret = QMessageBox.question(
            self, "Delete Word", "Do you want to delete the word?")
        if ret == QMessageBox.Yes:
            self.database.deleteWord("id", id)
            self.createWordTable(self.database.searchWord())
            QMessageBox.about(self, "Delete Word",
                              "Deleted word successfully!")

    def initSearchWord(self):
        self.fwfDialog.clear()
        self.fwfDialog.show()
        if self.fwfDialog.exec_():
            searchTerm = self.fwfDialog.getSearchTerm().strip()
            if searchTerm != "":
                self.createWordTable(self.database.searchWord(searchTerm))

    @QtCore.pyqtSlot(QPoint)
    def rightClickMenu(self, pos):
        it = self.dataTable.itemAt(pos)
        if it is None:
            return

        menu = QMenu()
        edit_action = menu.addAction("&Edit Word")
        view_action = menu.addAction("&View Word")
        delete_action = menu.addAction("&Delete Word")
        action = menu.exec_(self.dataTable.viewport().mapToGlobal(pos))

        if action == edit_action:
            self.initEditWord()
        if action == view_action:
            self.initViewWord()
        if action == delete_action:
            self.initDeleteWord()

    def createWordTable(self, data):
        if data == None:
            return
        self.dataTable.clear()
        self.dataTable.setRowCount(len(data))
        self.dataTable.setColumnCount(5)
        c = 0
        for row in data:
            (id, name, pos, meaning, example) = row
            nameItem = QTableWidgetItem(str(name))
            posItem = QTableWidgetItem(str(pos))
            meanItem = QTableWidgetItem(str(meaning))
            exText = QTableWidgetItem(str(example))
            self.dataTable.setItem(c, 0, nameItem)
            self.dataTable.setItem(c, 1, posItem)
            self.dataTable.setItem(c, 2, meanItem)
            self.dataTable.setItem(c, 3, exText)
            self.dataTable.setItem(c, 4, QTableWidgetItem(str(id)))
            c = c + 1

        # self.dataTable.horizontalHeader().setStretchLastSection(True)
        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Disable editable property
        self.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataTable.setColumnWidth(1, 100)
        # self.dataTable.resizeRowsToContents()
        self.dataTable.setColumnHidden(4, True)
        self.dataTable.setHorizontalHeaderLabels(
            ["Name", "POS", "Meaning", "Example", "ID"])

    def searchTextOnChange(self):
        searchTerm = self.searchText.text().strip()
        if searchTerm != "":
            self.createWordTable(self.database.searchWord(searchTerm))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.addWordBtn = QPushButton("Add Word")
        self.addWordBtn.setFixedSize(200, 30)
        self.addWordBtn.clicked.connect(self.initAddWord)

        # self.editWordBtn = QPushButton("Edit Word")
        # self.editWordBtn.setFixedSize(200, 30)
        # self.editWordBtn.clicked.connect(self.initEditWord)
        #
        # self.deleteWordBtn = QPushButton("Delete Word")
        # self.deleteWordBtn.setFixedSize(200, 30)
        # self.deleteWordBtn.clicked.connect(self.initDeleteWord)

        self.dataTable = QTableWidget()
        self.createWordTable(self.database.searchWord())

        self.searchText = QLineEdit()
        self.searchText.setFixedWidth(400)
        self.searchText.textChanged.connect(self.searchTextOnChange)

        layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(self.addWordBtn)
        # row1.addWidget(self.editWordBtn)
        # row1.addWidget(self.deleteWordBtn)

        row2 = QHBoxLayout()
        searchTermLabel = QLabel("Search term: ")
        searchTermLabel.setFixedWidth(300)
        row2.addWidget(searchTermLabel, 0, Qt.AlignRight)
        row2.addWidget(self.searchText, 0, Qt.AlignLeft)

        layout.addLayout(row2, 1)
        layout.addLayout(row1, 0)
        layout.addWidget(self.dataTable)

        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dd = DDApp()
    if(app.exec_()):
        dd.database.closeDB()
        sys.exit()
    # sys.exit(app.exec_())
