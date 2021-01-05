import sqlite3


def pkgs_dictionary2database(pkgs_dicts, pkgs_db_file):
    conn = sqlite3.connect(pkgs_db_file)
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
    c = conn.cursor()

    c.execute(f"""
            CREATE TABLE IF NOT EXISTS 'packages'
            (pkg_name text,
             pkg_url text,
             pkg_summary text,
             installer_name text,
             installer_url text,
             anaconda_ver text,
             python_ver text,
             pkg_ver text,
             pkg_included BOOLEAN)
           """)
    conn.commit()

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
    return None