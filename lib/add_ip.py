import re

from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from ui.add_ui import Ui_Form
from ui.netwok import add_ip

font_command = QFont()
font_command.setFamily("Arial")
font_command.setPointSize(8)


sernum = ''
mask = ''
manyc = ''
MASK_RULE = r'255.255.255.24[08]|255.255.255.224|255.255.255.192|255.255.255.128|255.255.255.0|255.255.255.252'

class Add_Ui(QWidget, Ui_Form):
    def __init__(self):
        super(Add_Ui, self).__init__()
        self.setupUi(self)
        self.textEdit.setFont(font_command)

        self.textEdit.setDisabled(True)
        self.pushButton.clicked.connect(self.push_add)

    @pyqtSlot()
    def push_add(self):
        global  sernum, mask, manyc
        sernum = self.ser_num_line.text()
        mask = self.mask_line.text()
        manyc = self.how_many_line.text()

        if not sernum:
            QMessageBox.about(self, '服务器编号不能为空', '服务器编号不能为空, 请输入服务器编号！')
            return

        if not mask:
            QMessageBox.about(self, '子网掩码不能为空', '子网掩码不能为空，请输入子网掩码！')
            return

        if not manyc:
            QMessageBox.about(self, '请输入要分配多少个C段', '请输入要分配多少个C段！')
            return

        if len(mask) < 3:
            if not mask.isdigit():
                QMessageBox.about(self, '子网掩码填写错误', '子网掩码填写错误, 请输入正确子网掩码！')
                return
            elif 30 < int(mask) or 24 > int(mask):
                QMessageBox.about(self, '子网掩码填写错误', '子网掩码填写错误, 请输入正确子网掩码！')
                return

        if len(mask) > 2:
            if not re.match(MASK_RULE, mask):
                QMessageBox.about(self, '子网掩码填写错误', '子网掩码填写错误, 请输入正确子网掩码！')
                return

        if not manyc.isdigit():
            QMessageBox.about(self, '需要分配的数量错误', '分配数量需为数字且不能有小数点,请重新输入！')
            return

        if int(manyc) > 32:
            QMessageBox.about(self, '数量过多', '每次最多只能分配32C！')
            return

        run = Run_thr()
        self.textEdit.append('正在添加...')
        run.signal_ip.connect(self.addip)
        run.start()
        run.exec()

    def addip(self, inting):
        if inting == 1:
            QMessageBox.about(self, '机器编号输入错误', '机器编号输入错误, 请重新输入！')
            self.textEdit.append('机器编号错误...')
            return
        elif inting == 2 or inting == 3:
            QMessageBox.about(self, '%s的IP段不足' % self.mask_line.text(),
                              '暂时无法分配出%s的IP段' % (self.mask_line.text()))
            self.textEdit.append('IP段不足...')
            return
        elif inting == 4:
            self.textEdit.append('添加完毕...')

class Run_thr(QThread):
    signal_ip = pyqtSignal(int)
    def __init__(self):
        super(Run_thr, self).__init__()

    def run(self):
        self.signal_ip.emit(add_ip(num=sernum, mask=mask, manyc=manyc))