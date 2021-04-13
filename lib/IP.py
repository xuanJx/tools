import re
import string

NETWORK = {
            '30': ['255.255.255.252', 0],
            '29': ['255.255.255.248', 4],
            '28': ['255.255.255.240', 12],
            '27': ['255.255.255.224', 28],
            '26': ['255.255.255.192', 60],
            '25': ['255.255.255.128', 124],
            '24': ['255.255.255.0', 254]
}

def ipaddr_mask(ip):
    mask = ip_split(ip)[-1]
    return NETWORK.get(mask)[0]

def ip_split(ip):
    return ip.split('/')

def ipadd_split(ip):
    ipadd = ip_split(ip)
    return ipadd[0].split('.')

def ip_3byte(ip):
    ipa = ipadd_split(ip)
    ipa.pop()
    return join_ip(ipa)+'.'

def join_ip(ip):
    return '.'.join(ip)

def ipaddr_gateway(ip):
    ipa = ipadd_split(ip)
    ipa[3] = str(int(ipa[3]) + 1)
    return join_ip(ipa)

def ipaddr_main(ip):
    ipa = ipadd_split(ip)
    ipa[3] = str(int(ipa[3]) + 2)
    return join_ip(ipa)

def main_last(ip):
    ipa = ipaddr_main(ip)
    ipad = ipa.split('.')
    return ipad[3]

def count_ip(ip):
     ipaa = main_last(ip)
     numm = NETWORK.get(ip_split(ip)[-1])[-1]
     return str(int(ipaa)+int(numm))

def end_ip(ip):
    ipa = ipadd_split(ip)
    ipa[3] = count_ip(ip)
    return join_ip(ipa)

def isip(ip):
    ip_list = ipadd_split(ip)
    for i in ip_list:
        try:
            int(i)
        except:
            return False
    return True

def remove_n(iplist):
    for i in iplist:
        if i == '':
            iplist.remove('')
            return remove_n(iplist)
    return iplist

def print_ip(ip):
    if int(count_ip(ip)) - int(main_last(ip)) == 0:
        return ipaddr_main(ip)
    else:
        return ipaddr_main(ip)+'-'+count_ip(ip)

def aaa(ip):
    return ip.split(' -')[0]

strip_rule = string.punctuation + r' ！￥…（）—+'

ip_commd_format = 'for /L %i in ({fristip},1,{lastip}) do netsh interface ip add '\
                    'address "{ethernet}" {ip3byte}%i {netmask}'

centos_path = '/etc/sysconfig/network-scripts'

debian_path = '/etc/network/interfaces'

centos_ip_commd_format = 'echo -n -e "DEVICE={adapter}\\nONBOOT=yes\\nBOOTPROTO=static\\nIPADDR_START' \
                  '={fristip}\\nIPADDR_END={lastip}\\nCLONENUM_START={ip_num}\\nNETMASK={netmask}' \
                  '\\nARPCHECK=no" > {conf_path}/{range_file}'

debian_ip_commd_format = 'n={ip_count};for ((x={fristip_1};x<={lastip};x++));do echo -n -e "\\nauto {adapter}:$n\\niface ' \
                  '{adapter}:$n inet static\\n\\taddress {ip3byte}$x/{subnetmask}" >> {debian_path};let n++;done'

SHELL_AUTO_GET_ADAPTER = r"ADAPTER=`ip addr show|grep 'BROADCAST.* UP'|awk -F ':' {'print $2'}|sed -n '1p'|sed 's/[[:space:]]//g'`"

centos7restart = 'sed -i "s/\\\\\\\\|ifcfg-\.\*-range//g" /etc/init.d/network\nsystemctl daemon-reload\nsystemctl restart network\n'