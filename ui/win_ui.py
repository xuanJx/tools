from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from ui.win_gg import Ui_win_gg
from ui.linux_gg import Ui_Form

from lib.IP import *

font_command = QFont()
font_command.setFamily("Arial")
#font_command.setFamily("宋体")
font_command.setPointSize(8)

LANGUAGE = {
            'cn': ['本地连接', '以太网'],
            'en': ['Local Area Connection', 'Ethernet']
}

LINUX_NET = {
                'centos6': 'eth0',
                'centos7': 'enp1s0f0',
                'ubuntu': 'eno1',
                'debian': 'eno1',
}

class Win_ui(QWidget, Ui_win_gg):
    def __init__(self):
        super(Win_ui, self).__init__()
        self.setupUi(self)
        self.textEdit.setFont(font_command)
        self.ip_count = 0

        self.copybutton.clicked.connect(self.push_copybutton)
        self.encheck.clicked.connect(self.setting_change)
        self.win8radio.clicked.connect(self.setting_change)
        self.win12radio.clicked.connect(self.setting_change)

        self.setDefault()

    @pyqtSlot()
    def setting_change(self):
        self.interline.setText(self.setting_line())

    def setting_line(self):
        if self.encheck.isChecked():
            language = 'en'
        else:
            language = 'cn'

        if self.win8radio.isChecked():
            return LANGUAGE.get(language)[0]
        elif self.win12radio.isChecked():
            return LANGUAGE.get(language)[-1]
        return

    @pyqtSlot()
    def push_copybutton(self):
        clip = QApplication.clipboard()
        clip.setText(self.textEdit.toPlainText())

    def setDefault(self):
        self.win8radio.setChecked(True)
        self.setting_change()

    def clear_all(self):
        self.textEdit.setText('')
        self.setDefault()

    def ip_commd(self, ip_block):
        return ip_commd_format.format(fristip=main_last(ip_block), lastip=count_ip(ip_block),
                                      ethernet=self.interline.text(),
                                      ip3byte=ip_3byte(ip_block), netmask=ipaddr_mask(ip_block))

    def other_command_output(self, user, passwd):
        other_command = 'net user {username} {passwd}\n'.format(username=user, passwd=passwd)
        other_command += 'netsh advfirewall firewall add rule name="Allow ICMPv4 echo request IN"' \
                         ' protocol=icmpv4:8,any dir=in action=allow'
        return other_command

    def IP_commd(self, ip_block, user, passwd):
        block_list = [self.ip_commd(block) for block in ip_block]
        self.textEdit.setText('\n'.join(block_list)+'\n'+self.other_command_output(user, passwd))


class Linux_ui(QWidget, Ui_Form):
    def __init__(self):
        super(Linux_ui, self).__init__()
        self.setupUi(self)
        self.textEdit.setFont(font_command)
        self.linux_defaul()
        self.ip_count = 0
        self.count = 0

        self.centos6radio.clicked.connect(self.network_ada)
        self.centos7radio.clicked.connect(self.network_ada)
        self.ubunturadio.clicked.connect(self.network_ada)
        self.debianradio.clicked.connect(self.network_ada)

        self.auto_get_check.toggled.connect(lambda: self.adapter_status(self.auto_get_check))
        self.not_auto_get_check.toggled.connect(lambda: self.adapter_status(self.not_auto_get_check))

        self.copybutton.clicked.connect(self.copybutton_push)

    @pyqtSlot()
    def copybutton_push(self):
        clip = QApplication.clipboard()
        clip.setText(self.textEdit.toPlainText())

    @pyqtSlot()
    def adapter_status(self, status):
        if status == self.auto_get_check:
            if self.auto_get_check.isChecked():
                self.not_auto_get_check.setChecked(False)
                self.lineEdit.setDisabled(True)
            else:
                self.not_auto_get_check.setChecked(True)
                self.lineEdit.setDisabled(False)
        elif status == self.not_auto_get_check:
            if self.not_auto_get_check.isChecked():
                self.auto_get_check.setChecked(False)
                self.lineEdit.setDisabled(False)
            else:
                self.auto_get_check.setChecked(True)
                self.lineEdit.setDisabled(True)

    @pyqtSlot()
    def network_ada(self):
        self.network_adapter()
        self.lineEdit.setText(LINUX_NET[self.system])

    def network_adapter(self):
        self.is_auto_get = True if self.auto_get_check.isChecked() else False
        self.is_setup_adapter = True if self.not_auto_get_check.isChecked() else False

        if self.centos6radio.isChecked():
            self.system = 'centos6'
        elif self.centos7radio.isChecked():
            self.system = 'centos7'
        elif self.ubunturadio.isChecked():
            self.system = 'ubuntu'
        elif self.debianradio.isChecked():
            self.system = 'debian'

    def linux_defaul(self):
        self.centos6radio.setChecked(True)
        self.auto_get_check.setChecked(True)
        self.lineEdit.setDisabled(True)
        self.network_ada()

    def clear_all(self):
        self.textEdit.setText('')
        self.linux_defaul()

    def other_command_output(self, username, passwd):
        command_output = ''
        if self.system == 'centos6':
            command_output += 'service network restart\n'
        elif self.system == 'centos7':
            command_output += centos7restart
        elif self.system == 'ubuntu':
            command_output += '/etc/init.d/networking restart\n'
        elif self.system == 'debian':
            command_output += '/etc/init.d/networking restart\n'
        command_output += 'echo "{passwd}" | passwd --stdin {username}\n'.format(passwd=passwd,
                                                                                 username=username)
        command_output += 'history -c'
        return command_output

    def IP_commd(self, ip_block, username, passwd):
        self.network_adapter()
        if self.is_auto_get:
            adapter_name = '${ADAPTER}'
            self.textEdit.setText('')
            self.textEdit.setText(SHELL_AUTO_GET_ADAPTER)
        else:
            adapter_name = self.lineEdit.text()
            self.textEdit.setText('')

        if self.system == 'centos6':
            ip_commd_list = [self.ip_commd_centos(ip_block=block, adapter=adapter_name) for block in ip_block]
            self.textEdit.append('\n'.join(ip_commd_list)+'\n'+self.other_command_output(username, passwd=passwd))

        elif self.system == 'centos7':
            ip_commd_list = [self.ip_commd_centos(ip_block=block, adapter=adapter_name) for block in ip_block]
            self.textEdit.append('\n'.join(ip_commd_list)+'\n'+self.other_command_output(username, passwd=passwd))

        elif self.system == 'ubuntu':
            ip_commd_list = [self.ip_commd_debian(ip_block=block, adapter=adapter_name) for block in ip_block]
            self.textEdit.append('\n'.join(ip_commd_list)+'\n'+self.other_command_output(username, passwd=passwd))

        elif self.system == 'debian':
            self.textEdit.append('sed -i "/iface ${ADAPTER}/iauto ${ADAPTER}" /etc/network/interfaces')
            ip_commd_list = [self.ip_commd_debian(ip_block=block, adapter=adapter_name) for block in ip_block]
            self.textEdit.append('\n'.join(ip_commd_list)+'\n'+self.other_command_output(username, passwd=passwd))

    def ip_commd_centos(self, ip_block, adapter):
        commd = centos_ip_commd_format.format(adapter=adapter, fristip=ipaddr_main(ip_block),
                                              lastip=end_ip(ip_block), ip_num=self.ip_count,
                                              netmask=ipaddr_mask(ip_block), conf_path=centos_path,
                                              range_file='ifcfg-' + adapter + '-range' + str(self.count))

        self.count += 1
        self.ip_count += int(count_ip(ip_block)) - int(main_last(ip_block)) + 1

        return commd

    def ip_commd_debian(self, ip_block, adapter):
        debian_ip_commd_format = 'n={ip_count};for ((x={fristip_1};x<={lastip};x++));do echo -n -e "\\nauto {adapter}:$n\\niface ' \
                                 '{adapter}:$n inet static\\n\\taddress {ip3byte}$x/{subnetmask}" >> {debian_path};let n++;done'
        commd = debian_ip_commd_format.format(
                                              ip_count=str(self.ip_count), fristip_1=str(int(main_last(ip_block))+1),
                                              lastip=count_ip(ip_block), adapter=adapter,
                                              ip3byte=ip_3byte(ip_block), subnetmask=ip_split(ip_block)[-1],
                                              debian_path=debian_path
                                              )

        self.ip_count += int(count_ip(ip_block)) - int(main_last(ip_block)) + 1

        return commd