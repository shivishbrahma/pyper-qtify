import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QComboBox,
    QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
import translate
import logging

logging.basicConfig(level=logging.INFO)


class OnubadApp(QWidget):
    def __init__(self):
        super().__init__()
        self.clipboard = QCoreApplication.instance().clipboard()

        self.initUI()

    def initUI(self):
        # Create widgets
        self.inputText = QTextEdit(self)
        self.inputText.setFont(QFont("Nirmala UI", 10))

        self.outputText = QTextEdit(self)
        self.outputText.setReadOnly(True)
        self.outputText.setFont(QFont("Nirmala UI", 10))
        # On Click - Copy Its Contents to Clipboard
        self.outputText.copyAvailable.connect(self.copyText)

        self.translateButton = QPushButton("Translate", self)
        self.translateButton.clicked.connect(self.translateText)

        src_langs = map(
            lambda x: x[0] + " - " + x[1]["name"], translate.languages.items()
        )
        target_langs = map(
            lambda x: x[0] + " - " + x[1]["name"], translate.languages.items()
        )

        self.srclangSelect = QComboBox(self)
        self.srclangSelect.addItems(src_langs)

        self.targetlangSelect = QComboBox(self)
        self.targetlangSelect.addItems(target_langs)
        self.targetlangSelect.setCurrentIndex(1)

        # Set layout
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Input Text"))
        layout.addWidget(self.inputText)

        layout.addWidget(QLabel("Select Source Language"))
        layout.addWidget(self.srclangSelect)

        layout.addWidget(self.translateButton)

        layout.addWidget(QLabel("Select Target Language"))
        layout.addWidget(self.targetlangSelect)

        layout.addWidget(QLabel("Translated Text"))
        layout.addWidget(self.outputText)

        self.setLayout(layout)

        self.setWindowTitle("Onubad")
        self.setGeometry(100, 100, 400, 300)
        self.show()

    def translateText(self):
        input_text = self.inputText.toPlainText()
        src_lang = self.srclangSelect.currentText().split(" - ")[0]
        target_lang = self.targetlangSelect.currentText().split(" - ")[0]
        output_text = translate.translate(input_text, src_lang, target_lang)
        self.outputText.setText(output_text)

    def copyText(self):
        text = self.outputText.toPlainText()
        self.clipboard.setText(text)
        # On Copy - Show Message as Alert
        QMessageBox.information(self, "Onubad", "Copied to Clipboard!")
        
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OnubadApp()
    sys.exit(app.exec_())
