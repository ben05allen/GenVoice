# pyright: basic


import pytest
from unittest.mock import patch
from tempfile import NamedTemporaryFile, TemporaryDirectory

from genvoice import main


def test_main_success():
    # Simulate command-line arguments
    test_args = (
        "prog --invoice 1 --template path/to/tplt --destination path/to/dest".split()
    )

    with patch("sys.argv", test_args):
        pass
