#coding=utf-8
PACKAGE='mm_crawler'
VERSION=__import__(PACKAGE).__version__
DESCRIPTION="This crawler use to crawl http:www.22mm.cc"


from setuptools import setup

__author__="blond"

setup(
    name=PACKAGE,
    version=VERSION,
    packages=[PACKAGE,],
    author="blond",
    author_email="liqingair@gmail.com",
    url="https://github.com/sointux/mm_crawler",
    license='LGPL',
    install_requires=['requests>=2.3.0',],
    description=DESCRIPTION,
    entry_points={
        'console_scripts': [
            'mm_crawler = %s.run:main' % PACKAGE,
        ],
    }
)
