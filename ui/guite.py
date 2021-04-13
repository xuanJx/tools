import sys
import re
import random
import time

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow
from PyQt5.QtWidgets import *

from ui.ui_gg import Ui_MainWindow
from ui.win_ui import Win_ui, Linux_ui
from lib import IP
from lib.netwok import num_to_ip, ip_to_num, TEST_FORMAT
from lib.pswd import password_generate
from lib.sernum_dig import Ui_Dialog
from ui.remove_ui import Remove_Ui
from lib.add_ip import Add_Ui
from ui.switch_ui import Switch_Ui
from ui.route_ui import Route_Ui

font_songti = QFont()
font_songti.setFamily("宋体")
font_songti.setPointSize(15)
sernum = ''
serip = ''

UI_WINDOW = {
            'windows': ['3389', 'Administrator'],
            'linux': ['22', 'root']
}

class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('test')
        self.setWindowIcon(QIcon('text1.png'))

        self.system = 'windows'
        self.child_ui = None
        self.child_default()

        self.remove_ui = None
        self.add_ui = None
        self.switch_ui = None
        self.route_ui = None

        self.windowsButton.clicked.connect(self.win_push_button)
        self.liunxButton.clicked.connect(self.linux_push_button)
        self.routegenerateButton.clicked.connect(self.autoIP)
        self.generateButton.clicked.connect(self.push_generate)
        self.allclearButton.clicked.connect(self.pushButton_clear)
        self.ServercopyButton.clicked.connect(self.Servercopy_Button)
        self.removeIP_Button.clicked.connect(self.remove_ip)
        self.addIP_Button.clicked.connect(self.add_ip)
        self.switch_Button.clicked.connect(self.switch_ip)
        self.routeconfigButton.clicked.connect(self.route_ip)
        self.dial.hide()

    @pyqtSlot()
    def route_ip(self):
        ip_block = self.IPtextEdit.toPlainText()

        if not ip_block:
            QMessageBox.about(self, '没有IP', '没有输入所有IP块,请输入所有IP块')
            return

        self.route_ui = Route_Ui()
        self.route_ui.show()
        self.route_ui.ip_block = ip_block

    @pyqtSlot()
    def switch_ip(self):
        self.switch_ui = Switch_Ui()
        self.switch_ui.show()

    @pyqtSlot()
    def add_ip(self):
        self.add_ui = Add_Ui()
        self.add_ui.show()

    @pyqtSlot()
    def remove_ip(self):
        self.remove_ui = Remove_Ui()
        self.remove_ui.show()

    @pyqtSlot()
    def win_push_button(self):
        self.system = 'windows'
        self.child_default()

    @pyqtSlot()
    def linux_push_button(self):
        self.system = 'linux'
        self.child_default()

    def child_win(self):
        if self.child_ui:
            self.child_ui.hide()
        self.child_ui = Win_ui()
        self.gridLayout.addWidget(self.child_ui)
        self.child_ui.show()

    def child_linux(self):
        if self.child_ui:
            self.child_ui.hide()
        self.child_ui = Linux_ui()
        self.gridLayout.addWidget(self.child_ui)
        self.child_ui.show()

    def child_default(self):
        if self.system == 'windows':
            self.child_win()
        elif self.system == 'linux':
            self.child_linux()

        self.UsernamelineEdit.setText(UI_WINDOW[self.system][-1])
        self.PortlineEdit.setText(UI_WINDOW[self.system][0])

    def ui_default(self):
        self.IPtextEdit.setEnabled(True)
        self.SeverNamelineEdit.setEnabled(True)



    @pyqtSlot()
    def push_generate(self):
        main_ip, port, username, passwd, allip, block_list = (
                    self.get_mainip(), self.get_port(),
                    self.get_username(), self.get_passwd(),
                    self.get_allip(), self.get_allblock()
        )
        sernum = self.SeverNamelineEdit.text()

        self.PortlineEdit.setText(port)
        self.IP_lineEdit.setText(main_ip)
        self.UsernamelineEdit.setText(username)
        self.passwdlineEdit.setText(passwd)
        self.IPtextEdit.setText('\n'.join(block_list))

        self.child_ui.ip_count = 0
        self.child_ui.count = 0
        self.child_ui.IP_commd(block_list, username, passwd)
        self.servertextEdit.setText(TEST_FORMAT % (sernum, main_ip, port, username, passwd + '\n\n' + allip))

        self.autoNUM()

    def servertext(self):
        main_ip, port, username, passwd, allip, sernum = (
                    self.IP_lineEdit.text(), self.PortlineEdit.text(),
                    self.UsernamelineEdit.text(), self.passwdlineEdit.text(),
                    self.get_allip(), self.SeverNamelineEdit.text()
        )
        # sernum = self.SeverNamelineEdit.text()
        self.servertextEdit.setText(TEST_FORMAT % (sernum, main_ip, port, username, passwd + '\n\n' + allip))
        self.ui_default()

    def autoNUM(self):
        global serip

        serip = self.get_mainip()

        if not serip:
            QMessageBox.about(self, '没有IP', '请输入IP')
            return

        self.SeverNamelineEdit.setDisabled(True)
        self.IPtextEdit.setDisabled(True)
        thre3 = Run_th2()
        thre3.signal_ip.connect(self.iptonum)
        thre3.start()
        thre3.exec()

    def iptonum(self, name):
        sernum = self.SeverNamelineEdit.text()
        if not sernum:
            self.SeverNamelineEdit.setText(name)
            return self.servertext()
        if name == '1':
            QMessageBox.about(self, '此IP未分配', '此IP未分配到后台机器上！')
            self.SeverNamelineEdit.setText(name)
            return self.servertext()
        elif sernum.lower() != name.lower():
            QMessageBox.about(self, 'IP与输入编号不匹配', 'IP与输入的机器编号不匹配,自动修改为后台获取的机器编号')
            self.SeverNamelineEdit.setText(name)
            return self.servertext()
        else:
            return self.servertext()

    def get_username(self):
        return UI_WINDOW[self.system][-1]

    def get_allblock(self):
        return [IP.aaa(i) for i in IP.remove_n(self.IPtextEdit.toPlainText().split('\n'))]

    def get_allip(self):
        return '\n'.join([IP.print_ip(i) for i in self.get_allblock()])

    def get_mainip(self):
        mainip = self.get_allip().split('\n')[0]
        return mainip if not re.search('-', mainip) else mainip.split('-')[0]

    def get_port(self):
        if self.portcheckBox.isChecked():
            port = str(random.choice(list(range(10000, 65535))))
        else:
            port = self.PortlineEdit.text()
            if not port or not port.isdigit():
                QMessageBox.about(self, '端口输入值错误', '端口输入值不能为空或必须全为整数且范围在1~65535之间')
                port = UI_WINDOW[self.system][0]
            elif 1 > int(port) or int(port) > 65535:
                QMessageBox.about(self, '端口输入值错误', '端口输入值范围必须在整数1~65535之间')
                port = UI_WINDOW[self.system][0]

        return port

    def get_passwd(self):
        if self.passwdcheckBox.isChecked():
            passwd = password_generate(strong=True)
        else:
            passwd = password_generate(strong=False) if not self.passwdlineEdit.text() else self.passwdlineEdit.text()

        return passwd

    @pyqtSlot()
    def autoIP(self):
        global sernum
        sernum = self.SeverNamelineEdit.text()

        if not sernum:
            QMessageBox.about(self, '服务器编号不能为空', '服务器编号不能为空, 请输入服务器编号！')
            return

        self.IPtextEdit.setDisabled(True)
        self.SeverNamelineEdit.setDisabled(True)
        thre = Run_th1()
        thre.signal_num.connect(self.numtoip)
        thre.start()
        thre.exec()

    def numtoip(self, IPte):
        self.IPtextEdit.setText(IPte)
        tuor = self.IPtextEdit.toPlainText()
        if tuor == '1':
            QMessageBox.about(self, '服务器编号错误', '服务器编号输入错误, 请重新输入！')
            return self.ui_default()
        elif tuor == '':
            QMessageBox.about(self, '服务器未分配IP', '服务器未分配IP, 请重新输入！')
            return self.ui_default()
        else:
            QMessageBox.about(self, '成功获取', '获取完毕！')
            return self.ui_default()


    @pyqtSlot()
    def Servercopy_Button(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.servertextEdit.toPlainText())

    @pyqtSlot()
    def pushButton_clear(self):
        self.SeverNamelineEdit.setText('')
        self.PortlineEdit.setText('')
        self.IP_lineEdit.setText('')
        self.UsernamelineEdit.setText('')
        self.passwdlineEdit.setText('')
        self.IPtextEdit.setText('')
        self.servertextEdit.setText('')
        self.child_ui.clear_all()

class Run_th1(QThread):
    signal_num = pyqtSignal(str)
    def __init__(self):
        super(Run_th1, self).__init__()

    def run(self):
        self.signal_num.emit(num_to_ip(num=sernum))

class Run_th2(QThread):
    signal_ip = pyqtSignal(str)
    def __init__(self):
        super(Run_th2, self).__init__()

    def run(self):
        self.signal_ip.emit(ip_to_num(ip=serip))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWINdow = Main_Window()
    MainWINdow.show()
    sys.exit(app.exec_())