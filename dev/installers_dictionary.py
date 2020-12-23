from scrape_single_page import get_installer_dictionary
from pprint import pprint
from urllib.parse import urlparse

def build_full_dictionary(installers_url_list):
    installer_dicts = {}
    for installer_url in installers_url_list:
        split_path = urlparse(installer_url).path.split('/')
        if split_path[3] == 'old-pkg-lists':
            installer_id = '_'.join(s for s in split_path[4:] if s)
        else:
            installer_id = 'current_' + '_'.join(s for s in split_path[3:] if s)
        installer_dicts[installer_id] = get_installer_dictionary(installer_url)
    return installer_dicts

if __name__ == '__main__':
    pprint(build_full_dictionary(['https://docs.anaconda.com/anaconda/packages/old-pkg-lists/1.1/']))
    pprint(build_full_dictionary(['https://docs.anaconda.com/anaconda/packages/old-pkg-lists/2.0.1/py27/']))
    pprint(build_full_dictionary(['https://docs.anaconda.com/anaconda/packages/old-pkg-lists/4.0.0/py35/']))
    