# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from bs4 import BeautifulSoup
import requests
import re


# %%
url = 'https://docs.anaconda.com/anaconda/packages/old-pkg-lists/4.0.0/py34/'
r = requests.get(url)
s = BeautifulSoup(r.content)
current = s.find(class_='current reference internal') # Gets this page's Anaconda and Python versions
anaconda_v, python_v = re.findall(r'Packages included in Anaconda ([\d\.]*\d) for Python version ([\d\.]*\d)',current.string)[0]
display(anaconda_v, python_v)


# %%

current


# %%
type(current)


# %%
current.string


# %%



