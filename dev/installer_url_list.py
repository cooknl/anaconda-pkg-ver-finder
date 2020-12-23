from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin

def get_list_of_oldpkgs(url='https://docs.anaconda.com/anaconda/packages/oldpkglists/'):

    r = requests.get(url)
    s = BeautifulSoup(r.content)

    urljoin(url,'../old-pkg-lists/1.0/')

    installer_url_list = []
    for item in s.find('div',class_='toctree-wrapper compound').ul.find_all('li'):
        installer_url_list.append(urljoin(url,item.a.get('href')))
    
    return installer_url_list

if __name__ == '__main__':
    print(get_list_of_oldpkgs())


