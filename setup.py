from setuptools import setup, find_packages
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('edgar/__init__.py').read(),
    re.M
    ).group(1)

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name = 'edgar',
        packages = find_packages(), # this must be the same as the name above
        version = version,
        description = 'Scrape data from SEC\'s EDGAR',
        long_description = long_description,
        author = 'Joey Sham',
        author_email = 'sham.joey@gmail.com',
        url = 'https://github.com/joeyism/py-edgar', # use the URL to the github repo
        download_url = 'https://github.com/joeyism/py-edgar/archive/{}.tar.gz'.format(version),
        keywords = ['edgar', 'sec'], 
        install_requires = ['requests', 'lxml'],
        classifiers = [],
        )
