from PyQt5 import QtWidgets
from components.dialogs import CenteredDialog


class AddWordForm(CenteredDialog):

    def __init__(self, parent=None):
        super(AddWordForm, self).__init__(parent)
        self.posList = [
            "Noun(n.)",
            "Adjective(adj.)",
            "Verb(v.)",
            "Verb Transitive(v.t.)",
            "Verb Intransitive(v.i.)",
            "Adverb(adv.)",
            "Past Participle(pp.)",
            "Preposition(prep.)",
            "Pronoun(pron.)",
            "Exclamation(exclam.)",
        ]
        self.posList.sort()
        self.createAddWordForm()

        self.title = "Add Word Form - Devil's Dictionary"
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 600

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.initUI()

    def createAddWordForm(self):
        self.formGroupBox = QtWidgets.QGroupBox("Add Word")

        self.nameText = QtWidgets.QLineEdit()
        self.nameText.setPlaceholderText("Enter the word...")
        self.posCombo = QtWidgets.QComboBox()
        for pos in self.posList:
            self.posCombo.addItem(pos)

        self.meanText = QtWidgets.QTextEdit()
        self.meanText.setPlaceholderText("Enter the meaning...")
        self.exText = QtWidgets.QTextEdit()
        self.exText.setPlaceholderText("Enter the example...")

        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Name: "), self.nameText)
        layout.addRow(QtWidgets.QLabel("POS: "), self.posCombo)
        layout.addRow(QtWidgets.QLabel("Meaning: "), self.meanText)
        layout.addRow(QtWidgets.QLabel("Example: "), self.exText)
        self.formGroupBox.setLayout(layout)

    def initUI(self):
        if self.parent() is not None:
            self.left = self.parent().left
            self.top = self.parent().top
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.toCenter()

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


class FindWordForm(CenteredDialog):
    def __init__(self, parent=None):
        super(FindWordForm, self).__init__(parent)
        self.createFindWordForm()

        self.title = "Find Word Form - Devil's Dictionary"
        self.left = 10
        self.top = 10
        self.width = 520
        self.height = 240

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.initUI()

    def createFindWordForm(self):
        self.formGroupBox = QtWidgets.QGroupBox("Find Word")
        self.searchText = QtWidgets.QLineEdit()
        self.searchText.setPlaceholderText("Enter the search term...")

        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Search term"))
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
        self.toCenter()
