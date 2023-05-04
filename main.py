import sys
import openai
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow

from form import  Ui_MainWindow


class MyForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        self.setWindowModality(Qt.NonModal)
        self.setStyleSheet("background-color: #E8E8E8 ;\n"
                                         "border: 5px, white;\n"
                                         "border-radius: 4px;\n"
                                         "margin: 0px;")
        self.lineEdit.setStyleSheet("background-color: #EeEeEe;\n")
        self.pushButton.setStyleSheet("background-color: #EeEeEe;\n")
        self.textEdit.setStyleSheet("background-color: #EeEeEe;\n")
        self.statusBar().hide()
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc', ), self, self.close)
        QtWidgets.QShortcut(QtGui.QKeySequence('F1', ), self, self.showMinimized)

        self._startPos = None
        self._endPos = None
        self._tracking = False

        self.askthread = MyThread()
        self.askthread.sinOut.connect(self.show_answer)
        self.lineEdit.returnPressed.connect(self.ask)

    def ask(self):
        question = self.lineEdit.text()
        self.askthread.str = question
        self.askthread.start()
        self.pushButton.setEnabled(False)
        self.textEdit.setText("等待回答~~")

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None


    def show_answer(self, ans):
        # self.textEdit.setMarkdown(ans)
        self.textEdit.setText(ans)
        self.pushButton.setEnabled(True)

class MyThread(QThread):
    sinOut = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.str = ""
        self.conversation_list = []

    def run(self):
        openai.api_key = "xxxx"
        self.conversation_list.append({"role": "user", "content": self.str})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.conversation_list)

        self.sinOut.emit(response["choices"][0]["message"]["content"])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myform = MyForm()
    myform.show()
    sys.exit(app.exec_())
