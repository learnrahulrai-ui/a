from pathlib import Path

import pytest

from app import enforce_rate_limit, extract_pdf_text, looks_like_pdf, request_tracker


class TestLooksLikePdf:
    """Tests for looks_like_pdf function."""

    def test_valid_pdf_signature(self, temp_pdf_file):
        """Test that valid PDF files are recognized."""
        assert looks_like_pdf(Path(temp_pdf_file)) is True

    def test_invalid_pdf_signature(self, invalid_pdf_file):
        """Test that non-PDF files are rejected."""
        assert looks_like_pdf(Path(invalid_pdf_file)) is False


class TestExtractPdfText:
    """Tests for extract_pdf_text function."""

    def test_extract_from_valid_pdf(self, temp_pdf_file):
        """Test extracting text from valid PDF."""
        text = extract_pdf_text(Path(temp_pdf_file))
        # Should return a string (possibly empty for minimal PDF)
        assert isinstance(text, str)

    def test_extract_returns_string(self, invalid_pdf_file):
        """Test that invalid files return empty string gracefully."""
        text = extract_pdf_text(Path(invalid_pdf_file))
        assert isinstance(text, str)
        assert text == ""

    def test_max_chars_limit(self, temp_pdf_file):
        """Test that max_chars parameter is respected."""
        max_chars = 100
        text = extract_pdf_text(Path(temp_pdf_file), max_chars=max_chars)
        assert len(text) <= max_chars


class TestRateLimit:
    """Tests for enforce_rate_limit function."""

    def setup_method(self):
        """Clear request tracker before each test."""
        request_tracker.clear()

    def test_rate_limit_allows_requests_under_limit(self):
        """Test that requests under the limit are allowed."""
        client_ip = "192.168.1.1"
        # Should not raise for first 20 requests
        for _ in range(20):
            try:
                enforce_rate_limit(client_ip)
            except Exception:
                pytest.fail("Rate limit should allow 20 requests")

    def test_rate_limit_blocks_excess_requests(self):
        """Test that requests exceeding the limit are blocked."""
        client_ip = "192.168.2.2"
        # Make 20 requests (the limit)
        for _ in range(20):
            enforce_rate_limit(client_ip)

        # The 21st request should raise a 429
        from werkzeug.exceptions import TooManyRequests
        with pytest.raises(Exception):  # Will raise abort(429)
            enforce_rate_limit(client_ip)

    def test_rate_limit_per_ip(self):
        """Test that rate limits are per IP."""
        client_ip_1 = "192.168.1.1"
        client_ip_2 = "192.168.1.2"

        # Fill up the limit for IP 1
        for _ in range(20):
            enforce_rate_limit(client_ip_1)

        # IP 2 should still be able to make requests
        try:
            enforce_rate_limit(client_ip_2)
        except Exception:
            pytest.fail("Rate limit should be per-IP")
