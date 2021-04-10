# anaconda-pkg-ver-finder

Answers the age-old question: In which Anaconda Installer is this package included?

## Intent

Provided a package name, return the versions of the Anaconda Installer that include the package

## Process

`dev > main.py` runs the entire process

### Scrape Anaconda websites with "metalists" of URLs for pages with package lists

`dev > installer_urls_list.y > get_list_of_oldpkgs()`
`dev > installer_urls_list.y > get_list_of_current_pkgs()`

- Download website with `requests`
- Parse HTML with `beautifulsoup4`
- Explore structure with `bs4.BeautifulSoup().contents` and Chrome Developer View
- Identify pages and tags that have the desired content
  - Identifying pages varies with old v current packages
    - Identifying tags varies with Anaconda version (1.x, 2.0-2.2, 2.3+)

- Old packages: just use `requests` and `bs4` to pull from the unordered list `li`

- Current packages: use `<a>` tags in the table to get URLs

### Create full list of URLS of package lists

`dev > installer_urls_list.py > build_installer_urls_list()`

### Create roll-up dict of individual package list dicts

`dev > installers_dictionary.py > build_full_dictionary()`

#### Given a URL of a single page create a dict of installer packages metadata

`dev > scrape_single_page > get_installer_dictionary`

Dict includes

- anaconda version
- python version
- dict of packages
  - package name
  - package version
  - package included in installer file (if not, then separate download required)
  - package OS's supported
  - package link
  - package summary description

- Parse table and pull package names, etc into a dictionary that includes the anaconda version and python version
- Use the anaconda+python+OS from the URL as a unique ID for the package list
- Anaconda 1.x rando tables can be queried by just pulling all `<li>` from the table
  - 1.3+ tables use different format, and an `<em>` tag messes up using just Tag.string attribute, so used Tag.contents instead, which still requires some understanding of how contents are nested in a list

Sites:

- Old installers: <https://docs.anaconda.com/anaconda/packages/oldpkglists/>
  - Anaconda v1.x: `https://docs.anaconda.com/anaconda/packages/old-pkg-lists/[anaconda_version]`
        - Rando table of packages
    - Anaconda v2.x - v4.x: `https://docs.anaconda.com/anaconda/packages/old-pkg-lists/[anaconda_version]/[python_version]/`
      - Tidy table of packages
    - Anaconda v5+: `https://docs.anaconda.com/anaconda/packages/old-pkg-lists/[anaconda_version]/[python_version]_[OS_version]/`
      - Tidy table of packages
- Current installers: <https://docs.anaconda.com/anaconda/packages/pkg-docs/>
  - Rando table of `[python_version]_[OS_version]`
    - Tidy table of packages
- Archive of actual installers: <https://repo.anaconda.com/archive/>
  - Tidy table of installers

### Save installers dict as JSON file

`main.py` --> `installers.json`

- `json.dump()` to save to file
- `json.load()` to read from file

### Transform installer-primary dict of dicts to a package-primary dict of dicts

`dev > pkgs_dictionary.py > installers2pkgs_dictionary()`

- Build set of all packages mentioned in any of the lists
- Use package name as primary key for the dictionary of dictionaries
- `collections.defaultdict` for dictionary to avoid `KeyError`
- Nested defaultdict allows for flexibility, as not every installer package list has every package

```python
pkgs_dict = {p: defaultdict(lambda: defaultdict(lambda: defaultdict(str))) for p in all_pkg_set}
```

### Save package dictionary to JSON

`main.py` --> `pkgs.json`

### TODO

- Cross-reference to list of actual installers
- Save package dictionary to SQLite database
- Create Django front-end to interact with database
- Host site on AWS
- ???
- Profit!!

## Cool finds

### Deep unpacking: <https://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/#Deep_unpacking>

When you have a string `'greenlet0.4.0'` and you apply this regex pattern to it to separate out the package name and the version number, `re.findall(r'([\D]+)(\d[\.\d]+\d)',e)`, you get a tuple of strings nested inside of a list `[('greenlet', '0.4.0')]`.

You can use multiple assignment and `zip()` to get the elements, like this:

```python
pkg_name, pkg_version = zip(*re.findall(r'([\D]+)(\d[\.\d]+\d)',e))
print(pkg_name, pkg_version)

('greenlet',) ('0.4.0',)
```

But the elements are still "trapped" in individual tuples. Changing the assignment by wrapping the assigned variable names in parentheses doesn't help:

```python
(pkg_name), (pkg_version) = zip(*re.findall(r'([\D]+)(\d[\.\d]+\d)',e))
print(pkg_name, pkg_version)

('greenlet',) ('0.4.0',)
```

However, if you sneak in a trailing comma, you can tell python that the elements are in a tuple, and you'd like to extract the element from inside the tuple:

```python
(pkg_name,), (pkg_version,) = zip(*re.findall(r'([\D]+)(\d[\.\d]+\d)',e))
print("n:", pkg_name, "; v:", pkg_version)

n: greenlet ; v: 0.4.0
```
