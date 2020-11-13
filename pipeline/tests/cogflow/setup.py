#!/usr/bin/env python
import setuptools

requirements = ['apache-airflow', 'cognite-sdk']

setuptools.setup(
    name='cogflow',
    version='0.1.0',
    description='Hooks and operators for the Cognite API.',
    author='Denis Gontcharov',
    author_email='denis@gontcharov.dev',

    install_requires=requirements,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gontcharovd/cognite',
    license='MIT license'
)
