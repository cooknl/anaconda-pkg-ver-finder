import json
import pathlib
from installer_urls_list import build_installer_urls_list
from installers_dictionary import build_full_dictionary
from pkgs_dictionary import installers2pkgs_dictionary
from pkgs_database import pkgs_dictionary2database
from pprint import pprint
import sqlite3


# Filenames
installers_json_filename = 'installers.json'
pkgs_json_filename = 'pkgs.json'
pkgs_db_filename = 'pkgs.db'

# Path objects
installers_json_file = pathlib.PurePath(__file__).parents[0].joinpath(pathlib.PurePath(installers_json_filename))
pkgs_json_file = pathlib.PurePath(__file__).parents[0].joinpath(pathlib.PurePath(pkgs_json_filename))
pkgs_db_file = pathlib.PurePath(__file__).parents[0].joinpath(pathlib.PurePath(pkgs_db_filename))

# Build only what's missing
if not pathlib.Path(pkgs_db_file).is_file():
    print('no packages database')


    if not pathlib.Path(pkgs_json_file).is_file():
        print('no packages JSON file')


        if not pathlib.Path(installers_json_file).is_file():
            print('no installers JSON file')

            print('building list of urls')
            installer_url_list = build_installer_urls_list()

            print('building dictionary')
            installers_dicts = build_full_dictionary(installer_url_list)

            print('saving to file')
            with open(installers_json_file, 'w', encoding='utf-8') as f:
                json.dump(installers_dicts, f, ensure_ascii=False, indent=4)

        else: 
            print('loading from installers JSON file')

            with open(installers_json_file, 'r') as f:
                installers_dicts = json.load(f)

        print('building dictionary of packages')
            
        pkgs_dicts = installers2pkgs_dictionary(installers_dicts)

        print('saving to file')

        with open(pkgs_json_file, 'w', encoding='utf-8') as f:
            json.dump(pkgs_dicts, f, ensure_ascii=False, indent=4)

    else:
        print('loading from packages JSON file')

        with open(pkgs_json_file, 'r') as f:
            pkgs_dicts = json.load(f)

    print('building database of packages')
        
    pkgs_dictionary2database(pkgs_dicts, pkgs_db_file)

else: 
    print('packages database exists')
