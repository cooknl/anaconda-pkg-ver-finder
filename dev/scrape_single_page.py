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
        raw_pkg_list = [li.string for li in s.find('table').find_all('li')]
        
        installer['pkgs'] = {}
        for e in raw_pkg_list:
            try:
                if '*' in e:
                    included = False
                    e = e[:-2]
                else:
                    included = True
                if ('(' in e):
                    e = e.split('(')[0].strip()
                    linux_only = True
                else:
                    linux_only = False
                if ('.' not in e) and ('(' not in e) and (not any(map(str.isdigit, e))):
                    pkg_name = e
                    pkg_version = ''
                if any(map(str.isdigit, e)):
                    if len(e.split(' ')) > 1:
                        pkg_name, pkg_version = e.split(' ')

                    else:
                        (pkg_name,), (pkg_version,) = zip(*re.findall(r'([\D]+)(\d[\.\d]+\d)',e))
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

        installer['python'] = installer['pkgs']['python']['version'] # get from python pkg.version

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
