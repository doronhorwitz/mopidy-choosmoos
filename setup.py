from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-ChoosMoos',
    version=get_version('mopidy_choosmoos/__init__.py'),
    url='https://github.com/doronhorwitz/mopidy-choosmoos',
    license='MIT License',
    author='Doron Horwitz',
    author_email='doron@milktek.com',
    description='Mopidy extension to support the ChoosMoos NFC Spotify Music Player',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'gpiozero >= 1.5.0',
        'Mopidy >= 1.0',
        'peewee >= 3.9.2',
        'Pykka >= 1.1',
        'setuptools',
        'tornado',
    ],
    entry_points={
        'mopidy.ext': [
            'choosmoos = mopidy_choosmoos:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
