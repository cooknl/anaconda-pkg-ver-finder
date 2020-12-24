import json
import pathlib
from pprint import pprint
from collections import defaultdict

def installers2pkgs_dictionary(installers_dicts):

    all_pkg_set = set()
    for d in installers_dicts:
        if 'pkgs' in installers_dicts[d]:
            all_pkg_set.update(installers_dicts[d]['pkgs'])

    pkgs_dict = {p: defaultdict(lambda: defaultdict(lambda: defaultdict(str))) for p in all_pkg_set}

    for d in installers_dicts:
        if 'pkgs' in installers_dicts[d]:
            for p in installers_dicts[d]['pkgs']:
                pkgs_dict[p]['pkg_url'] = installers_dicts[d]['pkgs'][p]['link']
                pkgs_dict[p]['pkg_summary'] = installers_dicts[d]['pkgs'][p]['summary']
                pkgs_dict[p]['installers'][d]['installer_url'] = installers_dicts[d]['url']
                pkgs_dict[p]['installers'][d]['anaconda'] = installers_dicts[d]['anaconda']
                pkgs_dict[p]['installers'][d]['python'] = installers_dicts[d]['python']
                pkgs_dict[p]['installers'][d]['pkg_version'] = installers_dicts[d]['pkgs'][p]['version']
                pkgs_dict[p]['installers'][d]['pkg_included'] = installers_dicts[d]['pkgs'][p]['included']
    return pkgs_dict

if __name__ == 'main':
    print('I"m empty')