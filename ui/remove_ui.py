from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from ui.remove_gg import Ui_Form
from ui.netwok import *

font_command = QFont()
font_command.setFamily("Arial")
font_command.setPointSize(8)

sernum = ''
class Remove_Ui(QWidget, Ui_Form):
    def __init__(self):
        super(Remove_Ui, self).__init__()
        self.setupUi(self)
        self.textEdit.setFont(font_command)

        self.textEdit.setDisabled(True)
        self.pushButton.clicked.connect(self.push_remove)

    @pyqtSlot()
    def push_remove(self):
        global  sernum
        sernum = self.re_num_line.text()

        if not sernum:
            QMessageBox.about(self, '服务器编号不能为空', '服务器编号不能为空, 请输入服务器编号！')
            return

        run = Run_thr()
        self.textEdit.append('正在删除...')
        run.signal_ip.connect(self.removeip)
        run.start()
        run.exec()

    def removeip(self, status):
        if status == '1':
            QMessageBox.about(self, '机器编号输入错误', '后台查找不到此机器编号！')
            self.textEdit.append('机器编号输入错误！')
            return
        if status == '2':
            QMessageBox.about(self, '此服务器没有IP', '此服务器未分配IP！')
            self.textEdit.append('此服务器未分配IP！')
            return
        else:
            self.textEdit.append('删除完成！')

class Run_thr(QThread):
    signal_ip = pyqtSignal(str)
    def __init__(self):
        super(Run_thr, self).__init__()

    def run(self):
        self.signal_ip.emit(remove_ip(num=sernum))