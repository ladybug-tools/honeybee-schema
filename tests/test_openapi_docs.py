"""Test generating OpenAPI docs."""
import os

root = os.path.dirname(os.path.dirname(__file__))
os.chdir(root)


def test_gen_openapi():
    rc = os.system('python ./docs.py')
    assert rc == 0
