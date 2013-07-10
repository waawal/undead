#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as file:
    long_description = file.read()

setup(
    name='undead',
    version='0.1.1',
    url='https://github.com/waawal/undead',
    license='MIT',
    author='Daniel Waardal',
    author_email='waawal@boom.ws',
    description='Dead Easy UNIX Daemons!',
    long_description=long_description,
    py_modules=['undead'],
    zip_safe=True,
    install_requires=['logbook','python-daemon',],
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.0',
        #'Programming Language :: Python :: 3.1',
        #'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration',

    ]
)