#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Leigh McKenzie
# All rights reserved.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import setuptools

requirements = []

setup_requirements = [
    "pytest-runner"
]

test_requirements = [
    "pytest",
    "pytest-catchlog"
]

setuptools.setup(
    name="crossing",
    version="0.1.0",
    description="PEdestrian LIght CONtrolled (PELICAN) Crossing",
    # long_description=readme + "\n\n" + history,
    author="Leigh McKenzie",
    author_email="maccarav0@gmail.com",
    url="https://github.com/leighmck/PELICAN-crossing",
    packages=setuptools.find_packages(),
    package_dir={"crossing": "crossing"},
    entry_points={
        'console_scripts': [
            'PELICAN-crossing=crossing:main'
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords="crossing",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
)
