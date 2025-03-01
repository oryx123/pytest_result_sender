import time


def test_api():
    time.sleep(2.5)


def test_pass():
    assert 1 == 1


def test_fail():
    assert 1 == 2
