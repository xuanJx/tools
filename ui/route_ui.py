import sys

from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from ui.route_gg import Ui_Form
from ui.IP import *

font_command = QFont()
font_command.setFamily("Arial")
font_command.setPointSize(8)

class Route_Ui(QWidget, Ui_Form):
    def __init__(self):
        super(Route_Ui, self).__init__()
        self.setupUi(self)
        self.routeText.setFont(font_command)
        self.clientText.setFont(font_command)

        self.ip_block = ''

        self.gatewayRadio.setChecked(True)
        self.default_radio()

        self.copyButton.clicked.connect(self.copy_one)
        self.copyButton_2.clicked.connect(self.copy_two)
        self.gatewayRadio.clicked.connect(self.default_radio)
        self.staticRadio.clicked.connect(self.default_radio)
        self.generateButton.clicked.connect(self.push_generate)

    def default_radio(self):
        self.default()

    def push_generate(self):
        ip_listA = remove_n(self.ip_block.split('\n'))
        ip_list = [aaa(ip) for ip in ip_listA]

        self.clientText.setText('')

        for ip in ip_list:
            self.clientText.append(print_ip(ip) + '\n' + ipaddr_gateway(ip) + '\n' + ipaddr_mask(ip) + '\n')

        if self.gatewayRadio.isChecked():
            self.gateway_route(ip_list)
        elif self.staticRadio.isChecked():
            self.static_route(ip_list)

    def gateway_route(self, ip_list):
        self.routeText.setText('no ip address')
        self.routeText.append('ip address ' + ipaddr_gateway(ip_list[0]) + ' ' + ipaddr_mask(ip_list[0]))

        del ip_list[0]

        for ip in ip_list:
            self.routeText.append('ip address ' + ipaddr_gateway(ip) + ' ' + ipaddr_mask(ip) + ' ' + 'secondary')
        self.routeText.append('ip access-group ACL-DENY-SMTP-PORT25 in')
        self.routeText.append('no ip redirects\n' + 'no ip unreachables\n' + 'no ip proxy-arp\n' + 'no shutdown\n')

    def static_route(self, ip_list):
        vlan = self.VLANLine.text()
        client = self.clientLine.text()

        if not vlan:
            QMessageBox.about(self, '没有VLAN', '没有输入VLAN, 请输入VLAN！')
            return

        if not client:
            QMessageBox.about(self, '没有客户编号', '没有客户编号, 请输入客户编号！')
            return

        vlan = vlan.strip(strip_rule)
        client = client.strip(strip_rule)

        self.routeText.setText('interface vlan %s' % vlan)
        self.routeText.append('no ip address')
        self.routeText.append('ip address ' + ipaddr_gateway(ip_list[0]) + ' ' + ipaddr_mask(ip_list[0]))
        self.routeText.append('ip access-group ACL-DENY-SMTP-PORT25 in')
        self.routeText.append('no ip redirects\n' + 'no ip unreachables\n' + 'no ip proxy-arp\n' + 'no shutdown')
        self.routeText.append('exit')

        ip_0 = ip_list.pop(0)

        for ip in ip_list:
            self.routeText.append('ip route ' + ip + ' ' + ipaddr_mask(ip)
                                  + ' ' + ipaddr_main(ip_0) + ' ' + 'name v%s-1-%s' % (vlan, client))


    def copy_one(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.routeText.toPlainText())

    def copy_two(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.clientText.toPlainText())

    def default(self):
        if self.gatewayRadio.isChecked():
            self.VLANLine.setDisabled(True)
            self.clientLine.setDisabled(True)
        else:
            self.VLANLine.setDisabled(False)
            self.clientLine.setDisabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWINdow = Route_Ui()
    MainWINdow.show()
    sys.exit(app.exec_())
