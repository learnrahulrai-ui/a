import os
import tempfile
from pathlib import Path

import pytest

from app import app as flask_app


@pytest.fixture
def app():
    """Create and configure a test app."""
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret-key"
    return flask_app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def temp_pdf_file():
    """Create a temporary valid PDF file for testing."""
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as f:
        # Valid PDF header
        f.write(b'%PDF-1.4\n')
        f.write(b'%\xE2\xE3\xCF\xD3\n')
        f.write(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')
        f.write(b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n')
        f.write(b'3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << >> /MediaBox [0 0 612 792] >>\nendobj\n')
        f.write(b'xref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n')
        f.write(b'trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n200\n%%EOF\n')
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def invalid_pdf_file():
    """Create a temporary invalid PDF file for testing."""
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as f:
        f.write(b'This is not a PDF file')
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)
