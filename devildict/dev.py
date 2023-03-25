import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from components.dialogs import ViewWidget
from components.forms import AddWordForm, FindWordForm
import db


class DDDevApp(QtWidgets.QWidget):
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
                QtWidgets.QMessageBox.about(
                    self, "Add Word", "Added new word successfully!"
                )

    def initEditWord(self):
        if self.dataTable.currentRow() < 0:
            QtWidgets.QMessageBox.warning(self, "Edit Word", "Please select a word!")
            return
        r, c = self.dataTable.currentRow(), self.dataTable.currentColumn()
        id = self.dataTable.item(r, 4).text()
        row = self.database.getOneWord("id", id)
        if row != None:
            (id, name, pos, meaning, example) = self.database.getOneWord("id", id)
        else:
            QtWidgets.QMessageBox.about(
                self, "Edit Word", "Database cannot find the entry!"
            )
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
            QtWidgets.QMessageBox.about(self, "Edit Word", "Updated word successfully!")

    def initViewWord(self):
        if self.dataTable.currentRow() < 0:
            QtWidgets.QMessageBox.warning(self, "View Word", "Please select a word!")
            return
        r, c = self.dataTable.currentRow(), self.dataTable.currentColumn()
        id = self.dataTable.item(r, 4).text()
        row = self.database.getOneWord("id", id)
        if row != None:
            (id, name, pos, meaning, example) = self.database.getOneWord("id", id)
        else:
            QtWidgets.QMessageBox.about(
                self, "View Word", "Database cannot find the entry!"
            )
            return

        self.vwfDialog.setWordData(name, pos, meaning, example)
        self.vwfDialog.show()

    def initDeleteWord(self):
        if self.dataTable.currentRow() < 0:
            QtWidgets.QMessageBox.warning(self, "Delete Word", "Please select a word!")
            return

        currentRow = self.dataTable.currentRow()
        name = self.dataTable.item(currentRow, 0).text()
        row = self.database.getOneWord("id", id)
        if row != None:
            (id, name, pos, meaning, example) = self.database.getOneWord("id", id)
        else:
            QtWidgets.QMessageBox.about(
                self, "Delete Word", "Database cannot find the entry!"
            )
            return

        ret = QtWidgets.QMessageBox.question(
            self, "Delete Word", "Do you want to delete the word?"
        )
        if ret == QtWidgets.QMessageBox.Yes:
            self.database.deleteWord("id", id)
            self.createWordTable(self.database.searchWord())
            QtWidgets.QMessageBox.about(
                self, "Delete Word", "Deleted word successfully!"
            )

    def initSearchWord(self):
        self.fwfDialog.clear()
        self.fwfDialog.show()
        if self.fwfDialog.exec_():
            searchTerm = self.fwfDialog.getSearchTerm().strip()
            if searchTerm != "":
                self.createWordTable(self.database.searchWord(searchTerm))

    @QtCore.pyqtSlot(QtCore.QPoint)
    def rightClickMenu(self, pos):
        it = self.dataTable.itemAt(pos)
        if it is None:
            return

        menu = QtWidgets.QMenu()
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
            nameItem = QtWidgets.QTableWidgetItem(str(name))
            posItem = QtWidgets.QTableWidgetItem(str(pos))
            meanItem = QtWidgets.QTableWidgetItem(str(meaning))
            exText = QtWidgets.QTableWidgetItem(str(example))
            self.dataTable.setItem(c, 0, nameItem)
            self.dataTable.setItem(c, 1, posItem)
            self.dataTable.setItem(c, 2, meanItem)
            self.dataTable.setItem(c, 3, exText)
            self.dataTable.setItem(c, 4, QtWidgets.QTableWidgetItem(str(id)))
            c = c + 1

        # self.dataTable.horizontalHeader().setStretchLastSection(True)
        self.dataTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        # Disable editable property
        self.dataTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dataTable.setColumnWidth(1, 100)
        # self.dataTable.resizeRowsToContents()
        self.dataTable.setColumnHidden(4, True)
        # Set headers for table
        self.dataTable.setHorizontalHeaderLabels(
            ["Name", "POS", "Meaning", "Example", "ID"]
        )

    def searchTextOnChange(self):
        searchTerm = self.searchText.text().strip()
        if searchTerm != "":
            self.createWordTable(self.database.searchWord(searchTerm))

    def toCenter(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("assets/icon.jpg"))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.toCenter()

        self.addWordBtn = QtWidgets.QPushButton("Add Word")
        self.addWordBtn.setFixedSize(200, 30)
        self.addWordBtn.clicked.connect(self.initAddWord)

        # self.editWordBtn = QPushButton("Edit Word")
        # self.editWordBtn.setFixedSize(200, 30)
        # self.editWordBtn.clicked.connect(self.initEditWord)
        #
        # self.deleteWordBtn = QPushButton("Delete Word")
        # self.deleteWordBtn.setFixedSize(200, 30)
        # self.deleteWordBtn.clicked.connect(self.initDeleteWord)

        self.dataTable = QtWidgets.QTableWidget()
        self.createWordTable(self.database.searchWord())

        self.searchText = QtWidgets.QLineEdit()
        self.searchText.setPlaceholderText("Enter the search term...")
        self.searchText.setFixedWidth(400)
        self.searchText.textChanged.connect(self.searchTextOnChange)

        layout = QtWidgets.QVBoxLayout()

        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(self.addWordBtn)
        # row1.addWidget(self.editWordBtn)
        # row1.addWidget(self.deleteWordBtn)

        row2 = QtWidgets.QHBoxLayout()
        searchTermLabel = QtWidgets.QLabel("Search term: ")
        searchTermLabel.setFixedWidth(300)
        row2.addWidget(searchTermLabel, 0, Qt.AlignRight)
        row2.addWidget(self.searchText, 0, Qt.AlignLeft)

        layout.addLayout(row2, 1)
        layout.addLayout(row1, 0)
        layout.addWidget(self.dataTable)

        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dd = DDDevApp()
    if app.exec_():
        dd.database.closeDB()
        sys.exit()
