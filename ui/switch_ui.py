from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from ui.switch_gg import Ui_Form
from ui.netwok import *

font_command = QFont()
font_command.setFamily("Arial")
font_command.setPointSize(8)

ser_num1 = ''
ser_num2 = ''

class Switch_Ui(QWidget, Ui_Form):
    def __init__(self):
        super(Switch_Ui, self).__init__()
        self.setupUi(self)
        self.textEdit.setFont(font_command)

        self.textEdit.setDisabled(True)
        self.pushButton.clicked.connect(self.push_switch)

    @pyqtSlot()
    def push_switch(self):
        global ser_num1, ser_num2

        ser_num1 = self.ser_num_one.text()
        ser_num2 = self.ser_num_two.text()

        if not ser_num1 or not ser_num2:
            QMessageBox.about(self, '机器编号不能为空', '机器编号不能为空，请重新输入！')
            return

        if ser_num1.lower() == ser_num2.lower():
            QMessageBox.about(self, '机器编号相同', '输入的两台机器编号相同，请重新输入！')
            return

        run = Run_thr()
        self.textEdit.append('正在转移IP...')
        run.signal_ip.connect(self.switchip)
        run.start()
        run.exec()

    def switchip(self, string):
        if string == '1':
            QMessageBox.about(self, '机器编号错误', '后台无法查询到需要转移IP的机器编号！')
            return
        elif string == '2':
            QMessageBox.about(self, '查询不到IP', '需要转移IP的机器编号下未分配IP！')
            return
        elif string == '3':
            QMessageBox.about(self, '机器编号错误', '后台无法查询到需要添加转移IP的机器编号！')
            return
        elif string == '4':
            self.textEdit.append('转移IP完毕！')


class Run_thr(QThread):
    signal_ip = pyqtSignal(str)
    def __init__(self):
        super(Run_thr, self).__init__()

    def run(self):
        self.signal_ip.emit(switch_ip(num1=ser_num1, num2=ser_num2))