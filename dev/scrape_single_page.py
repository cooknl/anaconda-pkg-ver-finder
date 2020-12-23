from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint

def get_installer_dictionary(url='https://docs.anaconda.com/anaconda/packages/old-pkg-lists/4.0.0/py35/'):

    installer = {}
    installer['url'] = url

    r = requests.get(url)
    s = BeautifulSoup(r.content, features="lxml")

    url_parts = url.split('/')
 
    installer['anaconda'] = url_parts[6]

    if (installer['anaconda'].split('.')[0] == '1'):
        pass

    elif (float(installer['anaconda'][:3]) < 2.2):
        
        installer['python'] = s.find('div', class_='section').p.string.split(' ')[-1]

        pkg_table = s.find('table', class_='docutils', border='1')

        installer['pkgs'] = {}
        for row in pkg_table.tbody.find_all('tr')[1:]:
            columns = row.find_all('td')
            pkg_name = columns[0].string
            installer['pkgs'][pkg_name] = {}
            installer['pkgs'][pkg_name]['link'] = '' 
            installer['pkgs'][pkg_name]['version'] = columns[1].string 
            installer['pkgs'][pkg_name]['summary'] = columns[2].string 
            if columns[3].string == 'True':
                installer['pkgs'][pkg_name]['included'] = True
            else:
                installer['pkgs'][pkg_name]['included'] = False
    else:
        installer['python'] = s.find('div', class_='section').p.string.split(' ')[-1]

        pkg_table = s.find('table', class_='docutils', border='1')

        installer['pkgs'] = {}
        for row in pkg_table.find_all('tr')[1:]:
            columns = row.find_all('td')
            pkg_name = columns[0].a.string
            installer['pkgs'][pkg_name] = {}
            installer['pkgs'][pkg_name]['link'] = columns[0].a.get('href') 
            installer['pkgs'][pkg_name]['version'] = columns[1].string 
            installer['pkgs'][pkg_name]['summary'] = columns[2].string 
            if columns[3].i:
                installer['pkgs'][pkg_name]['included'] = True
            else:
                installer['pkgs'][pkg_name]['included'] = False

    # # installer_includes = installer.copy()
    # # installer_includes['pkgs'] = dict(filter(lambda elem: elem[1]['included'], installer['pkgs'].items()))

    # # installer_not_includes = installer.copy()
    # # installer_not_includes['pkgs'] = dict(filter(lambda elem: not elem[1]['included'], installer['pkgs'].items()))



    return installer

if __name__ == '__main__':
    pprint(get_installer_dictionary('https://docs.anaconda.com/anaconda/packages/old-pkg-lists/2.0.1/py27/'))
