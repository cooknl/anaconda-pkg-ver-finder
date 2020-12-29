from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from pprint import pprint

def get_list_of_oldpkgs(url='https://docs.anaconda.com/anaconda/packages/oldpkglists/'):

    r = requests.get(url)
    s = BeautifulSoup(r.content, features="lxml")

    installer_url_list = []
    for item in s.find('div',class_='toctree-wrapper compound').ul.find_all('li'):
        installer_url_list.append(urljoin(url,item.a.get('href')))
    
    return installer_url_list

def get_list_of_current_pkgs(url='https://docs.anaconda.com/anaconda/packages/pkg-docs/'):

    r = requests.get(url)
    s = BeautifulSoup(r.content, features="lxml")

    installer_url_list = []
    for item in s.find('table').find_all('a'):
        installer_url_list.append(urljoin(url,item.get('href')))   
    return installer_url_list

def build_installer_urls_list():
    installer_urls_list = []

    installer_urls_list.extend(get_list_of_oldpkgs())

    installer_urls_list.extend(get_list_of_current_pkgs())

    return installer_urls_list

if __name__ == '__main__':
    pprint(get_list_of_oldpkgs())
    pprint(get_list_of_current_pkgs())
    pprint(build_installer_urls_list())


