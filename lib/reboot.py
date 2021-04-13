import requests
from bs4 import BeautifulSoup

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}

sessionn = requests.Session()

url = 'https://admin.esited.com/admin.php?login=true'


data = {'login': 'true',
        'username': 'Hans',
        'password': 'Esited.!@#'}

response = sessionn.post(url, headers=headers, data=data)
def reboot(num):
    global response
    if response.status_code == 200:
        url = 'https://admin.esited.com/admin.php?act=search&words=%' % num
        sessionn.post(url, data=data)