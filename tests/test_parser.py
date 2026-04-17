import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.parser import extract_text_from_pdf


def test_parser_invalid_file():
    with pytest.raises(ValueError):
        extract_text_from_pdf("nonexistent_file.pdf")


def test_parser_non_pdf():
    # Create a fake non-PDF file
    fake_path = "/tmp/fake_resume.txt"
    with open(fake_path, 'w') as f:
        f.write("This is not a PDF")
    with pytest.raises(ValueError):
        extract_text_from_pdf(fake_path)
    os.remove(fake_path)
