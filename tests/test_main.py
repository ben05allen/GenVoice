# pyright: basic


import pytest
from unittest.mock import patch
from freezegun import freeze_time

from genvoice import main
import genvoice.processor


@pytest.fixture()
def test_template(tmp_path):
    template_text = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Minimal Jinja2 Test</title>
</head>
<body>
  <h1>Hello, Jinja2!</h1>
  <p>This is a minimal template for testing purposes.</p>
  <p>{{ test_string }}</p>
</body>
</html>
        """

    template_file = tmp_path / "test.html"
    template_file.write_text(template_text)

    yield str(template_file)


def mock_get_template_data(i: int):
    return {"test_string": f"invoice {i}"}


def test_main_success(test_template, tmp_path, monkeypatch):
    template_file = test_template
    dest_folder = tmp_path / "dest"
    monkeypatch.setattr(genvoice.processor, "get_template_data", mock_get_template_data)

    # Simulate command-line arguments
    test_args = f"prog -i 1 -t {template_file} -d {dest_folder}".split()

    with patch("sys.argv", test_args), freeze_time("2020-01-01 12:00:00"):
        main()

        assert mock_get_template_data(1) == {"test_string": "invoice 1"}
        assert (dest_folder / "invoice_1_20200101120000.pdf").exists()
