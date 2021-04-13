import sys
import re
import random
import time
import pysnooper

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow
from PyQt5.QtWidgets import *

from ui.ui_gg import Ui_MainWindow
from ui.win_ui import Win_ui
from lib import IP
from lib.netwok import num_to_ip, ip_to_num, TEST_FORMAT
from lib.pswd import password_generate

font_songti = QFont()
font_songti.setFamily("宋体")
font_songti.setPointSize(15)
sernum = ''
UI_WINDOW = {
            'windows': ['3389', 'Administrator'],
            'linux': ['22', 'root']
}
@pysnooper.snoop()
class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('test')
        self.setWindowIcon(QIcon('text1.png'))

        self.system = 'windows'
        self.child_ui = None
        self.windowsButton.clicked.connect(self.child_win)
        self.liunxButton.clicked.connect(self.child_linux)
        self.routegenerateButton.clicked.connect(self.autoIP)
        self.generateButton.clicked.connect(self.push_generate)
        self.allclearButton.clicked.connect(self.pushButton_clear)
        self.ServercopyButton.clicked.connect(self.Servercopy_Button)
        self.dial.hide()

    @pyqtSlot()
    def child_win(self):
        if self.child_ui:
            self.child_ui.hide()
        self.child_ui = Win_ui()
        self.gridLayout.addWidget(self.child_ui)
        self.child_ui.show()

    @pyqtSlot()
    def child_linux(self):
        self.child_ui.hide()

    def ui_default(self):
        self.IPtextEdit.setEnabled(True)
        self.SeverNamelineEdit.setEnabled(True)

    def numtoip(self, IPte):
        self.IPtextEdit.setText(IPte)
        tuor = self.IPtextEdit.toPlainText()
        if tuor == '':
            QMessageBox.about(self, '服务器编号错误', '服务器编号输入错误或服务器未分配IP, 请重新输入！')
            return self.ui_default()
        else:
            return self.ui_default()

    @pyqtSlot()
    def push_generate(self):
        sernum = self.SeverNamelineEdit.text()
        # ip_block = self.IPtextEdit.toPlainText()

        username, main_ip, iptext, port, passwd = (
                                          self.get_username(),
                                          self.get_mainip(), self.get_allip(),
                                          self.get_port(), self.get_passwd()
)

        self.servertextEdit.setText(TEST_FORMAT % sernum, main_ip, port, username, passwd + '\n' + iptext)

    def get_username(self):
        return UI_WINDOW.get(self.system)[-1]

    def get_allip(self):
        all_block = IP.remove_n(self.IPtextEdit.toPlainText().split('\n'))

        all_ip_list = [IP.aaa(i) for i in all_block]
        ip_list = [IP.print_ip(i) for i in all_ip_list]

        return '\n'.join(ip_list)

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
            elif 1 > int(port) or int(port) > 65535:
                QMessageBox.about(self, '端口输入值错误', '端口输入值范围必须在整数1~65535之间')
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
        # time.

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

class Run_th1(QThread):
    signal_num = pyqtSignal(str)
    def __init__(self):
        super(Run_th1, self).__init__()

    def run(self):
        self.signal_num.emit(num_to_ip(num=sernum))

class Run_th2(QThread):
    signal_ip = pyqtSignal(str)
    def __init__(self):
        super(RUN_th2, self).__init__()

    def run(self):
        self.signal_ip.emit(ip_to_num(ip=serip))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWINdow = Main_Window()
    MainWINdow.show()
    sys.exit(app.exec_())