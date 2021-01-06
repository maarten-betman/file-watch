from file_watch.handle_gef import  post_gef_file
from .TestUtils import TestUtils


def test_post_gef_file():
    file = TestUtils.get_local_test_file("S30-35_CPT-PRE-C8A-07.GEF")
    r = post_gef_file(file=file)
    assert r.status_code in [200, 409]
