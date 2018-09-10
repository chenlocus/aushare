from setuptools import setup, find_packages
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

long_desc = """
auShare
===============

Target Users
--------------

* financial market analyst of Australia
* learners of financial data analysis with pandas/NumPy
* people who are interested in Australian financial data

Installation
--------------

    pip install aushare
    
Upgrade
---------------

    pip install aushare --upgrade
    

"""

def read_install_requires():
    reqs = [
            'pandas>=0.22.0',
            'requests>=2.18.4',
            'beautifulsoup4>=4.6.0',
            'bs4>=0.0.1',
            'simplejson>=3.16.0',
            'lxml>=4.1.1',
            'jsonschema==2.6.0',
            'msgpack>=0.5.6',
            'pyzmq>=16.0.0'
            ]
    return reqs


setup(
    name='aushare',
    version=read('aushare/VERSION.txt'),
    description='A utility for crawling financial data of ASX stocks',
    long_description = long_desc,
    author='Hao Chen',
    author_email='chenlocus@hotmail.com',
    license='BSD',
    url='https://github.com/chenlocus/aushare',
    install_requires=read_install_requires(),
    keywords='Australian Financial Data',
    classifiers=['Development Status :: 1 - Beta',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'License :: OSI Approved :: BSD License'],
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.csv', '*.txt']},
)