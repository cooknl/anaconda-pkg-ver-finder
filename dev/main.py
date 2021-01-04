import json
import pathlib
from installer_urls_list import build_installer_urls_list
from installers_dictionary import build_full_dictionary
from pkgs_dictionary import installers2pkgs_dictionary
from pprint import pprint
import sqlite3

installers_json_filename = 'installers.json'

installers_json_file = pathlib.PurePath(__file__).parents[0].joinpath(pathlib.PurePath(installers_json_filename))

if not pathlib.Path(installers_json_file).is_file():
    print('no installers file')

    print('building list of urls')
    installer_url_list = build_installer_urls_list()

    print('building dictionary')
    installers_dicts = build_full_dictionary(installer_url_list)

    print('saving to file')
    with open(installers_json_file, 'w', encoding='utf-8') as f:
        json.dump(installers_dicts, f, ensure_ascii=False, indent=4)

else: 
    print('loading from installers file')

    # Assumes existence of installers.json

    with open(installers_json_file, 'r') as f:
        installers_dicts = json.load(f)

pkgs_json_filename = 'pkgs.json'

pkgs_json_file = pathlib.PurePath(__file__).parents[0].joinpath(pathlib.PurePath(pkgs_json_filename))

if not pathlib.Path(pkgs_json_file).is_file():
    print('no packages file')

    print('building dictionary of packages')
        
    pkgs_dicts = installers2pkgs_dictionary(installers_dicts)

    print('saving to file')

    with open(pkgs_json_file, 'w', encoding='utf-8') as f:
        json.dump(pkgs_dicts, f, ensure_ascii=False, indent=4)

else:
    print('loading from packages file')

    with open(pkgs_json_file, 'r') as f:
        pkgs_dicts = json.load(f)


# https://devopsheaven.com/sqlite/databases/json/python/api/2017/10/11/sqlite-json-data-python.html

pkgs_db_filename = 'pkgs.db'
pkgs_db_file = pathlib.PurePath(__file__).parents[0].joinpath(pathlib.PurePath(pkgs_db_filename))

conn = sqlite3.connect(pkgs_db_file)
sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
c = conn.cursor()

for pkg in pkgs_dicts.keys():
    # pkg_url, pkg_summary, DICT installers
    for installer in pkgs_dicts[pkg]['installers'].keys():
        # installer_url, anaconda, python, pkg_version, pkg_included
        parameters = (  pkg,
                        pkgs_dicts[pkg]['pkg_url'],
                        pkgs_dicts[pkg]['pkg_summary'],
                        installer,
                        pkgs_dicts[pkg]['installers'][installer]['installer_url'],
                        pkgs_dicts[pkg]['installers'][installer]['anaconda'],
                        pkgs_dicts[pkg]['installers'][installer]['python'],
                        pkgs_dicts[pkg]['installers'][installer]['pkg_version'],
                        pkgs_dicts[pkg]['installers'][installer]['pkg_included'],
                        )
        query = "INSERT INTO packages VALUES ( ?,?,?, ?,?,?, ?,?,? )"
        c.execute(query, parameters)
conn.commit()

conn.close()