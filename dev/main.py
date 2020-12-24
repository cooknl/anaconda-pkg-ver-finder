import json
import pathlib
from installer_urls_list import build_installer_urls_list
from installers_dictionary import build_full_dictionary
from pkgs_dictionary import installers2pkgs_dictionary
from pprint import pprint


json_filename = 'installers.json'

json_file = pathlib.PurePath(__file__).parents[0].joinpath(pathlib.PurePath(json_filename))

if not pathlib.Path(json_file).is_file():
    print('not file')

    print('building list of urls')
    installer_url_list = build_installer_urls_list()

    print('building dictionary')
    installer_dicts = build_full_dictionary(installer_url_list)

    print('saving to file')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(installer_dicts, f, ensure_ascii=False, indent=4)

else: 
    print('is file')

    # Assumes existence of installers.json

    with open(json_file, 'r') as f:
        installers_dicts = json.load(f)

pkgs_dicts = installers2pkgs_dictionary(installers_dicts)

json_filename = 'pkgs.json'

json_file = pathlib.PurePath(__file__).parents[0].joinpath(pathlib.PurePath(json_filename))

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(pkgs_dicts, f, ensure_ascii=False, indent=4)


