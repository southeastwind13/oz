import pytest

@pytest.fixture
def object_one():
    return 1

class TestOne:
    def test_order(self, object_one):
        assert object_one == 1