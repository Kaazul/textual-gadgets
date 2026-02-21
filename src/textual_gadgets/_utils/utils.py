"""Utility functions"""

from importlib.metadata import PackageNotFoundError, version


def get_version() -> str:
    """Reads the version of the package"""
    try:
        return version("textual-gadgets")
    except PackageNotFoundError:
        return "unknown"
