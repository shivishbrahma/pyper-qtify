import io
import sys
from PyQt5.QtCore import QBuffer, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PIL import Image
import time
from helpers import AlDiModel


class Canvas(QLabel):
    def __init__(self, width=600, height=300):
        super().__init__()

        self.last_x, self.last_y = None, None
        self.penColor = QColor("#000")
        self.paperColor = QColor("#fff")
        self.penWidth = 8

        pixmap = QPixmap(width, height)
        pixmap.fill(self.paperColor)
        self.setPixmap(pixmap)

    def setPenColor(self, c) -> None:
        self.penColor = QColor(c)

    def setPenWidth(self, w) -> None:
        self.penWidth = w

    def setPaperColor(self, c) -> None:
        self.paperColor = QColor(c)

    def clearCanvas(self) -> None:
        self.pixmap().fill(self.paperColor)
        self.update()

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        painter = QPainter(self.pixmap())
        pen = painter.pen()
        pen.setWidth(self.penWidth)
        pen.setColor(self.penColor)
        pen.setCapStyle(Qt.RoundCap)  # For rounded lines
        painter.setPen(pen)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


class AlDiRecogApp(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.model = AlDiModel('aldi.tflite')

        self.title = "Digit Recog"
        self.left = 10
        self.top = 10
        self.width = 720
        self.height = 480

        self.initUI()
        self.center()

    def center(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def initUI(self) -> None:

        layout = QVBoxLayout()

        row1 = QHBoxLayout()

        self.drawingCanvas = Canvas(360, 480)
        self.drawingCanvas.setPenWidth(10)

        self.last_x, self.last_y = None, None

        self.resultPanel = QLabel("**Welcome to the Alpha Digit !**")
        self.resultPanel.setTextFormat(Qt.MarkdownText)
        self.resultPanel.setAlignment(Qt.AlignCenter)

        row1.addWidget(self.resultPanel)
        row1.addWidget(self.drawingCanvas)

        row2 = QHBoxLayout()

        self.clearBtn = QPushButton("Clear")
        self.clearBtn.setFixedWidth(120)
        self.clearBtn.clicked.connect(self.clearCanvas)

        self.recogBtn = QPushButton("Recognise")
        self.recogBtn.setFixedWidth(120)
        self.recogBtn.clicked.connect(self.recogniseCanvas)

        row2.addWidget(self.clearBtn)
        row2.addWidget(self.recogBtn)

        layout.addLayout(row1, 0)
        layout.addLayout(row2, 0)

        self.setLayout(layout)
        self.show()

    def clearCanvas(self):
        self.drawingCanvas.clearCanvas()
        self.resultPanel.setText("**Welcome to the Alpha Digit !**")

    def recogniseCanvas(self):
        qImage = self.drawingCanvas.pixmap().toImage()
        qBuffer = QBuffer()
        qBuffer.open(QBuffer.ReadWrite)
        qImage.save(qBuffer, "PNG")
        pImage = Image.open(io.BytesIO(qBuffer.data()))
        # filename = time.strftime("img%Y%m%d%H%M%S.png")
        # pImage.save(filename)
        self.resultPanel.setText("Finding....")
        data = self.model.recogniseImage(pImage)
        time.sleep(1)
        self.resultPanel.setText(
            f"**Result:**\n\n{data['label_id']} ({round(data['prob']*100,3)}%)"
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ada = AlDiRecogApp()
    if app.exec_():
        sys.exit()