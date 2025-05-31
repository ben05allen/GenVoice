from freezegun import freeze_time
from pypdf import PdfReader
import pytest
from unittest.mock import patch

import genvoice


@pytest.fixture()
def test_template(tmp_path):
    template_text = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Minimal Jinja2 Test</title>
  <style>@page {size: A4;};</style>
</head>
<body>
  <h1>Test Invoice PDF<h1>
  <p>{{ test_string }}</p>
  <p>This is a minimal template for testing purposes.</p>
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
    monkeypatch.setattr(genvoice, "get_template_data", mock_get_template_data)

    # Simulate command-line arguments
    test_args = f"prog -i 1 -t {template_file} -d {dest_folder}".split()

    with patch("sys.argv", test_args), freeze_time("2020-01-01 12:00:00"):
        genvoice.main()

    pdf_file = dest_folder / "invoice_1_20200101120000.pdf"
    reader = PdfReader(pdf_file)
    pdf_text = reader.pages[0].extract_text()

    assert pdf_file.exists()
    assert mock_get_template_data(1)["test_string"] in pdf_text
