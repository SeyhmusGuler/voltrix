"""Test basic package functionality."""

import voltrix


def test_package_has_version() -> None:
    """Test that the package has a version attribute."""
    assert hasattr(voltrix, "__version__")
    assert isinstance(voltrix.__version__, str)


def test_version_format() -> None:
    """Test that version follows semantic versioning format."""
    version = voltrix.__version__
    # Should be in format X.Y.Z or X.Y.Z.devN+... or similar
    assert "." in version
    parts = version.split(".")
    assert len(parts) >= 3 or "dev" in version
