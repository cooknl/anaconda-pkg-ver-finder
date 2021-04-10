from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint

def get_installer_dictionary(url='https://docs.anaconda.com/anaconda/packages/old-pkg-lists/4.0.0/py35/'):

    installer = {}
    installer['url'] = url

    r = requests.get(url)

    if r.status_code == 404:
        return None

    s = BeautifulSoup(r.content, features="lxml")

    url_parts = url.split('/')

    if url_parts[5] == 'old-pkg-lists':
        installer['anaconda'] = url_parts[6]
    else:
        installer['anaconda'] = 'current'

    if (installer['anaconda'] != 'current') and (float(installer['anaconda'][:3]) < 2):
        installer['pkgs'] = {}

        raw_pkg_list = [li.contents for li in s.find('table').find_all('li')]

        for e in raw_pkg_list:
            try:
                if '*' in e[0]:
                    included = False
                    e[0] = e[0][:-2]
                else:
                    included = True
                if ('(' in e[0]):
                    e[0] = e[0].split('(')[0].strip()
                    linux_only = True
                elif (len(e) > 1) and ('L' in e[1].contents[0]):
                    linux_only = True
                else:
                    linux_only = False
                if (len(e) > 1) and ('U' in e[1].contents[0]):
                    unix_only = True
                else:
                    unix_only = False
                if (len(e) > 1) and ('M' in e[1].contents[0]):
                    apple_only = True
                else:
                    apple_only = False
                if (len(e) > 1) and ('W' in e[1].contents[0]):
                    windows_only = True
                else:
                    windows_only = False
                if (len(e) > 1) and ('P' in e[1].contents[0]):
                    included = False
                else:
                    included = True
                if ('.' not in e[0]) and ('(' not in e[0]) and (not any(map(str.isdigit, e[0]))):
                    pkg_name = e[0]
                    pkg_version = ''
                if any(map(str.isdigit, e[0])):
                    if len(e[0].split(' ')) > 1:
                        pkg_name, pkg_version = e[0].strip().split(' ')

                    else:
                        (pkg_name,), (pkg_version,) = zip(*re.findall(r'([\D]+)(\d[\.\d]+\d)',e[0]))
            except:
                with open('error_log.txt','a') as f:
                    f.writelines(installer['url'])
                    pprint(s.find('table').find_all('li'),f)
                    pprint(raw_pkg_list,f)
                return None

            installer['pkgs'][pkg_name] = {}
            installer['pkgs'][pkg_name]['link'] = '' 
            installer['pkgs'][pkg_name]['version'] = pkg_version 
            installer['pkgs'][pkg_name]['summary'] = '' 
            installer['pkgs'][pkg_name]['included'] = included
            installer['pkgs'][pkg_name]['linux_only'] = linux_only
            installer['pkgs'][pkg_name]['apple_only'] = apple_only
            installer['pkgs'][pkg_name]['windows_only'] = windows_only
            installer['pkgs'][pkg_name]['unix_only'] = unix_only

        installer['python'] = installer['pkgs']['python']['version'] # get from python pkg.version

    elif (installer['anaconda'] != 'current') and (float(installer['anaconda'][:3]) < 2.2):
        
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

        installer['python'] = installer['pkgs']['python']['version'] # get from python pkg.version

    else:

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

        installer['python'] = installer['pkgs']['python']['version'] # get from python pkg.version

    # # installer_includes = installer.copy()
    # # installer_includes['pkgs'] = dict(filter(lambda elem: elem[1]['included'], installer['pkgs'].items()))

    # # installer_not_includes = installer.copy()
    # # installer_not_includes['pkgs'] = dict(filter(lambda elem: not elem[1]['included'], installer['pkgs'].items()))



    return installer

if __name__ == '__main__':
    pprint(get_installer_dictionary('https://docs.anaconda.com/anaconda/packages/py3.7_win-64/'))
