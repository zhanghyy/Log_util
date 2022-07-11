# -*- coding: utf-8 -*-
# @Time : 2021/9/8 15:17
# @Author :Ben
# @Email :
from setuptools import setup, find_packages
import os





install_requires = [
    'concurrent-log-handler==0.9.9',
]

if os.name == 'nt':
    install_requires.append('pywin32')

setup(
    name='easy_log',  #
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    install_requires=install_requires
)
