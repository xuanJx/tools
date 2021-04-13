import requests
import re
from bs4 import BeautifulSoup
import random
from lib.IP import *

'''
num_to_ip: search ip with server num
ip_to_num: search server num with ip
add_ip: add_ip for server 
remove_ip: from server num remove all ip
switch_ip: transfer the ip of one server to another
'''

FIND_LINK_R = r'\shref="(.*)">Remove</a>'
FIND_IPMI_LINK = '<a href="(http://\d+.\d+.\d+.\d+)"'
FIND_ADD_LINK = r'\shref="(.*)">Add</a>'
FIND_VALUE = r'.+ESITED.+|.+WH04.+|.+ZeroDDOS.+|.+WHDOT.+|.+Esited \d.+|.+ESITED104.+|.+ABCDE03.+|.+WH03.+'\
    '|.+esited 105.+|.+ABCDE04.+|.+SAL03.+'

'''find server name: div', class_="box_c_content cf"'''

FIND_V = r'option value="(\d+)"'
FIND_N = r'0/24\s.(\d+).'

ADD_DATA = {
'assign': 'true',
'server_id': None,
'client_id': None,
'ip_pool_id': None,
'type': 'classless',
'block_size': None,
'network_ip': None,
'route_block': 'true',
}

block_sizeA = {
               '30': 4,
               '29': 8,
               '28': 16,
               '27': 32,
               '26': 64,
               '25': 128,
               '24': 258,
               }

block_sizeB = {
            '255.255.255.252': 4,
            '255.255.255.248': 8,
            '255.255.255.240': 16,
            '255.255.255.224': 32,
            '255.255.255.192': 64,
            '255.255.255.128': 128,
            '255.255.255.0': 256
}

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}

sessionn = requests.Session()

url = 'https://admin.esited.com/admin.php?login=true'


data = {'login': 'true',
        'username': 'Hans',
        'password': 'Esited.!@#'}

response = sessionn.post(url, headers=headers, data=data)

def get_response(num):
    global response
    if response.status_code == 200:
        url = 'https://admin.esited.com/admin.php?act=search&words=%s' % num
        response = sessionn.get(url, headers=headers)
        return 1 if re.search('no results found, please refine', response.text) else response.text

def num_to_ip(num):
        res = get_response(num)
        if res == 1:
            return '1'
        else:
            ress = re.findall(r'\d+[.]\d+[.]\d+[.]\d+[/]\d\d', str(res))
            return '\n'.join(ress)

def ip_to_num(ip):
        res = get_response(ip)
        if res == 1:
            return '1'
        else:
            ress = re.findall(r'Server Information - <strong>(\w+\d+)[<]', str(res))
            return ress[0]

def remove_ip(num):
        listA = []
        response = get_response(num)
        if response == 1:
            return '1'
        else:
            res = BeautifulSoup(response, 'html.parser')
            for item in res.find_all('a'):
                    listA.append(re.findall(FIND_LINK_R, str(item)))
            listB = remove_none(listA)
            if not listB:
                return '2'
            else:
                post_remove(listB)

def remove_none(listA):
        for i in listA:
                if not i:
                        listA.remove(i)
                        return remove_none(listA)
        return url_place(listA)

def url_place(listA):
        listB = []
        for i in listA:
            listB.append(i[0].replace('amp;', '', 3))
        return listB

def post_remove(listB):
        for url in listB:
                sessionn.post(url=url, headers=headers, data=data)

def add_ip(num, mask, manyc):
    listA = []
    res = get_response(num)
    soup = BeautifulSoup(res, 'html.parser')
    for item in soup.find_all('div', class_='msg_box msg_error'):
        if re.search('no results found, please refine', str(item)):
            return 1
        else:
            break

    for item in soup.find_all('div', 'box_c_heading'):
        listA.extend(re.findall(FIND_ADD_LINK, str(item)))

    add_url = listA[0].replace('amp;', '', 2)

    ADD_DATA['server_id'] = add_url.split('=')[-1]

    if len(mask) > 6:
        ADD_DATA['block_size'] = block_sizeB[mask]
    else:
        ADD_DATA['block_size'] = block_sizeA[mask]

    listt = test(ADD_DATA['block_size'])

    if not listt:
        return 2

    idx = 0

    for i in range(int(manyc)):
            ADD_DATA['ip_pool_id'] = int(listt[idx])
            add_response = sessionn.post(url=add_url, headers=headers, data=ADD_DATA)
            idx += 2
            if re.search('could not find IP assignment', add_response.text):
                return 3
    return 4

def test(maskk):
    listA = []

    add_ip_url = 'https://admin.esited.com/admin.php?act=servers&do=ip_assign&server_id=7'

    new_res = sessionn.get(url=add_ip_url, headers=headers, data=data)
    soupA = BeautifulSoup(new_res.text, 'html.parser')
    for item in soupA.find_all('option'):
        listA.extend(re.findall(FIND_VALUE, str(item)))
    removeaaa(listA)

    listC = []

    remove_ccc(listA, maskk)

    for i in listA:
        listC.extend(re.findall(FIND_V, i))

    return listC

def remove_ccc(listA, maskk):
    for i in listA:
        if int(re.findall(FIND_N, i)[0]) < maskk:
            listA.remove(i)
            return remove_ccc(listA, maskk)
    return listA

def removeaaa(url_list):
    for i in url_list:
        if not i:
            url_list.remove(i)
            return removeaaa(url_list)
    return url_list

def switch_ip(num1, num2):
    num1_block = num_to_ip(num1)
    if num1_block == '1':
        return '1'
    elif num1_block == '':
        return '2'
    else:
        num1_ip = num1_block.split('\n')
    new_num1_ip = []
    for i in num1_ip:
        new_num1_ip.append(ip_split(i))

    remove_ip(num1)

    for new_ip in new_num1_ip:
        swit = switch_ip_add(num2=num2, netIP=new_ip[0], mask=new_ip[1])
        if swit == '2':
            return '3'
        else:
            return '4'

def switch_ip_add(num2,netIP, mask):
    listA = []
    res = get_response(num2)
    if res == 1:
        return '2'
    else:
        soup = BeautifulSoup(res, 'html.parser')

    for item in soup.find_all('div', 'box_c_heading'):
        listA.extend(re.findall(FIND_ADD_LINK, str(item)))

    add_url = listA[0].replace('amp;', '', 2)

    server_id = add_url.split('=')[-1]

    ADD_DATA['server_id'] = server_id
    ADD_DATA['block_size'] = block_sizeA[mask]
    ADD_DATA['network_ip'] = netIP
    ADD_DATA['ip_pool_id'] = find_pool_ip(netIP)

    sessionn.post(url=add_url, headers=headers, data=ADD_DATA)
    return 3

def find_pool_ip(netIP):
    listA = []
    add_ip = 'https://admin.esited.com/admin.php?act=servers&do=ip_assign&server_id=7'

    new_res = sessionn.get(url=add_ip, headers=headers, data=data)
    soupA = BeautifulSoup(new_res.text, 'html.parser')
    for item in soupA.find_all('option'):
        listA.extend(re.findall(FIND_VALUE, str(item)))
    removeaaa(listA)

    FIND_NET_IP = ip_3byte(netIP)
    listC = []
    for i in listA:
        listC.extend(re.findall(FIND_V+'.+'+FIND_NET_IP, i))

    return listC[0]



TEST_FORMAT = '''机器编号：%s
主    IP：%s
端    口：%s
用 户 名：%s
密    码：%s

'''
