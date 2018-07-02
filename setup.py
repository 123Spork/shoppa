#!/usr/bin/env python
from distutils.core import setup

setup(
    name='shoppa',
    version='7.8.0',
    packages=['.'],
    install_requires=[
        'Flask==0.10.1',
        'Flask-RESTful==0.2.12',
        'Flask-WTF==0.10.3',
        'requests==2.4.3',
        'pymysql==0.7.9'
        'sqlalchemy==1.1.3'
    ],
)
