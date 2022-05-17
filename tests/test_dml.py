import os
import pytest


test_case_file = './prepared_dml.sql'


def load_test_cases(file_path):
    cases = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file_input:
            cases = list(map(str.strip, file_input))
    return cases


def exec_query(conn, sql_str):
    conn.execute(sql_str)
    return 'success'


def start_session(conn, test_case_file):
    test_cases = load_test_cases(test_case_file)
    for i, case in enumerate(test_cases):
        print("Test Case No.{0}: \n`{1}`".format(i, case))
        curr_result = exec_query(conn, case)
        print("Execution result: \n{0}".format(curr_result))
    return True


@pytest.fixture(scope='session', params=[test_case_file])
def exec(request, starrocks_connection):
    try:
        status = start_session(starrocks_connection, request.param)
    except:
        status = False
    assert status


def test_exec(exec):
    print("PASSED")


if __name__ == '__main__':
    pwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pwd)
    test_script_file = __file__.split('/')[-1]
    pytest.main(['-s', test_script_file])