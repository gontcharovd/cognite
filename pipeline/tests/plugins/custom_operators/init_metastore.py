#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess


def init_metastore(path: str):
    """Initialize an SQLite Airflow metastore.

    The metastore is created in the current folder

    Args:
        dirname
    Returns:
        Path to the Airflow metastore
    """
    uri = f'sqlite:///{path}'

    env = os.environ.copy()
    env['AIRFLOW__CORE__SQL_ALCHEMY_CONN'] = uri
    env['AIRFLOW__CORE__LOAD_EXAMPLES'] = 'False'
    env['AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS'] = 'False'

    init_metastore = subprocess.Popen(['airflow', 'db', 'init'], env=env)
    init_metastore.wait()
    print(f'Created Airflow metastore in: {path}')
    return uri


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    metastore_path = os.path.join(dirname, 'airflow.db')
    init_metastore(metastore_path)
