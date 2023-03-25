from PyQt5 import QtWidgets


class CenteredDialog(QtWidgets.QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def toCenter(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class ViewWidget(CenteredDialog):
    def __init__(self, parent=None):
        super(ViewWidget, self).__init__(parent)
        self.createViewWordForm()

        self.title = "View Word - Devil's Dictionary"
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 600

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.accept)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.initUI()

    def createViewWordForm(self):
        self.formGroupBox = QtWidgets.QGroupBox("View Word")
        self.nameLabel = QtWidgets.QLineEdit()
        self.nameLabel.setReadOnly(True)
        self.posLabel = QtWidgets.QLineEdit()
        self.posLabel.setReadOnly(True)
        self.meanLabel = QtWidgets.QTextEdit()
        self.meanLabel.setReadOnly(True)
        self.exLabel = QtWidgets.QTextEdit()
        self.exLabel.setReadOnly(True)
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Name: "), self.nameLabel)
        layout.addRow(QtWidgets.QLabel("POS: "), self.posLabel)
        layout.addRow(QtWidgets.QLabel("Meaning: "), self.meanLabel)
        layout.addRow(QtWidgets.QLabel("Example: "), self.exLabel)
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
        self.toCenter()
