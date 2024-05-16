from analyzer import *

def test_get_stat():
    result = getStat("https://www.youtube.com/watch?v=jNQXAC9IVRw")
    assert len(result) == 3