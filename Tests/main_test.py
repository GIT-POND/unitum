from fastapi.testclient import TestClient
from App.main import app  # import app instance

test_client = TestClient(app)


def test_root():
    response = test_client.get("/",)
    assert response.status_code == 200


'''
import pytest


def sum_vals(v1, v2):
    return v1+v2


@pytest.fixture
def initial():
    # return classCONSTRUCTOR()
    return 1


@pytest.mark.parametrize("val1, val2, check", [
    (3, 2, 5),
    (4, 4, 8),
    (3, 6, 9),
    (9, 2, 11)
])
def test_one(val1, val2, check):
    assert sum_vals(val1, val2) == check


@pytest.mark.parametrize("val1, val2, check", [
    (3, 2, 10),
    (4, 4, 10),
    (3, 6, 10),
    (9, 2, 10)
])
def test_two(val1, val2, check):
    with pytest.raises(Exception):
        assert sum_vals(val1, val2) == check
'''
