import os
import sys
import pytest


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)


from starrocks_dialect.starrocks import StarrocksDialect


test_schema = 'information_schema'
test_table = 'character_sets'
test_column = 'CHARACTER_SET_NAME'
metadata_labels = ('name', 'type', 'nullable', 'default', 'extra')
metadata_store_type = dict
query_str = 'select CHARACTER_SET_NAME,DEFAULT_COLLATE_NAME, \
            DESCRIPTION from information_schema.character_sets;'


sr = StarrocksDialect()


@pytest.fixture
def test_has_schema(starrocks_connection):
    assert sr.has_schema(starrocks_connection, test_schema)


@pytest.fixture
def test_has_table(starrocks_connection):
    assert sr.has_table(starrocks_connection, test_table, test_schema)


@pytest.fixture
def test_get_schema_names(starrocks_connection):
    assert test_schema in sr.get_schema_names(starrocks_connection)


@pytest.fixture
def test_get_table_names(starrocks_connection):
    assert test_table in sr.get_table_names(starrocks_connection, test_schema)


@pytest.fixture
def test_get_columns(starrocks_connection):
    # check if the method works at first
    assert sr._get_table_columns(starrocks_connection, test_table, test_schema)
    labels = ('name', 'type', 'nullable', 'default', 'extra')
    column_exists = False
    columns = sr.get_columns(starrocks_connection, test_table, test_schema)
    for column in columns:
        # check if metadata of the column is a dict
        assert isinstance(column, dict)
        # check if metadata contains all labels
        for label in labels:
            assert label in column
        # check if the given column name exists
        if test_column == column.get('name'):
            column_exists = True
    assert column_exists


@pytest.fixture
def test_query(starrocks_connection):
    result = sr.query(starrocks_connection, query_str)
    # check if the result is iterable
    assert isinstance(result, (list, tuple))
    # check if there is any record in the result
    assert len(result) > 0
    # there're 3 columns selected in the query
    assert len(result[0]) == 3


def test_above():
    test_has_schema
    test_get_schema_names
    test_get_table_names
    test_has_table
    test_get_columns
    test_query
    print("PASSED")


if __name__ == '__main__':
    pwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pwd)
    test_script_file = __file__.split('/')[-1]
    pytest.main(['-s', test_script_file])