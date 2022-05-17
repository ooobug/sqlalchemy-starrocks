import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.dialects import registry


def compose_connection_str(host, port, username, password, database=None, charset='utf8'):
    prefix = 'starrocks://'
    port = port or 9030
    password = password or ''
    if database:
        suffix = '/%s' % database
    else:
        suffix = ''
    if charset:
        suffix += '/?charset=%s' % charset
    url = '{0}:{1}@{2}:{3}'.format(username, password, host, port)
    conn_str = prefix + url + suffix
    return conn_str


@pytest.fixture(scope='session')
def starrocks_connection_str():
    host = 'localhost' 
    port = 9030
    username = 'root'
    password = ''
    database = ''
    return compose_connection_str(host, port, username, password, database)


@pytest.fixture(scope='session')
def starrocks_dialect():
    driver = 'starrocks'
    dialect = 'starrocks_dialect.starrocks'
    module = 'StarrocksDialect'
    registry.register(driver, dialect, module)


@pytest.fixture(scope='session')
def starrocks_engine(starrocks_dialect, starrocks_connection_str):
    # connection string: starrocks://<username>:<password>@<host>/<dbname>[?<options>]
    return create_engine(starrocks_connection_str)


@pytest.fixture(scope='session')
def starrocks_connection(starrocks_engine):
    conn = starrocks_engine.connect()
    print("Welcome to starrocks!")
    yield conn
    conn.close()
    print("Bye!")