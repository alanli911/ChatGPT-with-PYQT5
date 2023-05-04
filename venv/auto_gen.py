import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class ReplaceString(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("replace_string.ui", self)  # 加载GUI

        self.open_button.clicked.connect(self.open_directory)
        self.replace_button.clicked.connect(self.replace_string)

    def open_directory(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", os.path.expanduser("~"))
        if folder_path:
            self.folder_path.setText(folder_path)

    def replace_string(self):
        folder_path = self.folder_path.text()
        if not folder_path:
            QMessageBox.warning(self, "错误", "请选择一个文件夹")
            return

        old_str = self.old_string.text()
        if not old_str:
            QMessageBox.warning(self, "错误", "请输入旧字符串")
            return

        new_str = self.new_string.text()
        if not new_str:
            QMessageBox.warning(self, "错误", "请输入新字符串")
            return

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r+') as f:
                    content = f.read()
                    if old_str in content:
                        content = content.replace(old_str, new_str)
                        f.seek(0)
                        f.write(content)
                        f.truncate()


if __name__ == '__main__':
    app = QApplication([])
    window = ReplaceString()
    window.show()
    app.exec_()