# -*- coding: utf-8 -*-

import setuptools
import os

#--------------------------------------------------------------------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'simpleplots', '__version__.py'), 'r', encoding='utf-8') as f:
    file_data = [i.replace('\n', '').replace('\'', '').split(' = ') for i in f.readlines()]
    about = {k: v for k, v in file_data}

def readme(logo_end_line=0):
    """Extracts the logo from README file before pushing to PyPi."""

    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = ''.join(fh.readlines()[logo_end_line:])

    return long_description

classifiers = [
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Development Status :: 5 - Production/Stable",
    "Natural Language :: English",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Information Technology",
]

requires = [
    "pillow ~= 9.0.1",
]

#--------------------------------------------------------------------------------------------------------------

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    packages=['simpleplots'],
    py_modules=['base', 'figure', 'themes', 'ticker', 'utils', 'visuals'],
    include_package_data=True,
    package_data={'': ['*.ttf'], 'simpleplots': ['fonts/*.*']},
    classifiers=classifiers,
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=requires,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    project_urls={
        'Source': about['__url__'],
    },
)

#--------------------------------------------------------------------------------------------------------------
