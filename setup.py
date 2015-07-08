#!/usr/bin/env python
"""
Setup script
"""

from setuptools import setup


setup(
    name='is-it-in-rhel',
    description='A command line tool to find out if a package is in RHEL.',
    version='1.0',
    license='GPLv2+',
    download_url='https://pagure.io/releases/is-it-in-rhel',
    url='https://pagure.io/is-it-in-rhel',
    author='Pierre-Yves Chibon',
    author_email='pingou@pingoured.fr',
    py_modules=['is_it_in_rhel'],
    entry_points={
        'console_scripts': [
            "is-it-in-rhel=is_it_in_rhel:main",
        ]
    },
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later '
        '(GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
)
