from bs4 import BeautifulSoup
import requests
import re

def get_installer_dictionary(url='https://docs.anaconda.com/anaconda/packages/old-pkg-lists/4.0.0/py35/'):

    installer = {}
    r = requests.get(url)
    s = BeautifulSoup(r.content, features="lxml")

    url_parts = url.split('/')
    print(url_parts[6])


    # print(s.prettify())

    # current = s.find(class_='current reference internal') # Gets this page's Anaconda and Python versions
    # anaconda_v, python_v = re.findall(r'Packages included in Anaconda ([\d\.]*\d) for Python version ([\d\.]*\d)',current.string)[0]

 
    installer['anaconda'] = url_parts[6]

    if (installer['anaconda'].split('.')[0] == '1'):
        print(installer)
    else:
        installer['python'] = url_parts[6]

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
    print(get_installer_dictionary('https://docs.anaconda.com/anaconda/packages/old-pkg-lists/1.0/'))
    
