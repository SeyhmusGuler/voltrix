"""
VOLatility maTRIX - a python library for pricing formulas and models.
"""

try:
    from ._version import version as __version__  # type: ignore
except ImportError:
    # Fallback version if setuptools-scm hasn't generated _version.py yet
    __version__ = "0.0.0.post0"

__all__ = ["__version__"]
