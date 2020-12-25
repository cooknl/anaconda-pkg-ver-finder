# anaconda-pkg-ver-finder

Answers the age-old question: In which Anaconda Installer is this package included?

## Intent

Provided a package name, return the versions of the Anaconda Installer that include the package

## Process

### Scrape Anaconda website pages

- Download website with `requests`
- Parse HTML with `beautifulsoup4`
- Explore structure with `bs4.BeautifulSoup().contents` and Chrome Developer View
- Identify pages and tags that have the desired content
  - Identifying pages varies with old v current packages
    - Identifying tags varies with Anaconda version (1.x, 2.0-2.2, 2.3+)

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

### Create list of URLS of package lists

- Old packages: just use `requests` and `bs4` to pull from the unordered list

### Given a URL create a dict of desired content

- Parse table and pull package names, etc into a dictionary that includes the anaconda version and python version
- Use the anaconda+python+OS from the URL as a unique ID for the package list

### Create roll-up dict of individual package list dicts and save as JSON file

- `json.dump()` to save to file
- `json.load()` to read from file

### Transform installer-primary dict of dicts to a package-primary dict of dicts

- Build set of all packages mentioned in any of the lists
- Use package name as primary key for the dictionary of dictionaries
- `collections.defaultdict` for dictionary to avoid `KeyError`
- Nested defaultdict allows for flexibility, as not every installer package list has every package

```python
pkgs_dict = {p: defaultdict(lambda: defaultdict(lambda: defaultdict(str))) for p in all_pkg_set}
```

### Save package dictionary to JSON

### TODO

- Old packages v1.x: parse rando table
- New packages: pull from the "wide" table
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
