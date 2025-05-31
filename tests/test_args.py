import pytest
from unittest.mock import patch

from genvoice import arg_parser


def test_parse_args_required_arguments():
    # Simulate command-line arguments
    test_args = (
        "prog --invoice 1 --template path/to/tplt --destination path/to/dest".split()
    )

    with patch("sys.argv", test_args):
        args = arg_parser().parse_args()
        assert args.invoice == 1
        assert args.template == "path/to/tplt"
        assert args.destination == "path/to/dest"


def test_parse_args_short_flag_names():
    test_args = "prog -i 2 -t path/to/template -d path/to/destination".split()

    with patch("sys.argv", test_args):
        args = arg_parser().parse_args()
        assert args.invoice == 2
        assert args.template == "path/to/template"
        assert args.destination == "path/to/destination"


def test_parse_args_missing_required_invoice():
    test_args = "prog --template path/to/tplt --destination path/to/dest".split()

    with patch("sys.argv", test_args), pytest.raises(SystemExit):
        arg_parser().parse_args()  # should raise due to missing invoice number


def test_parse_args_missing_required_template():
    test_args = "prog --invoice 1 --destination path/to/dest".split()

    with patch("sys.argv", test_args), pytest.raises(SystemExit):
        arg_parser().parse_args()  # should raise due to missing template
