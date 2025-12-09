import os
import sys

import pytest

from utils import resource_path


def test_resource_path_returns_string():
    """Test that resource_path returns a string."""
    result = resource_path("assets/smiley.png")
    assert isinstance(result, str)


def test_resource_path_joins_relative_path():
    """Test that resource_path correctly joins the relative path."""
    relative = "assets/test.png"
    result = resource_path(relative)
    assert result.endswith(relative) or relative.replace("/", os.sep) in result


def test_resource_path_with_empty_string():
    """Test resource_path with an empty string."""
    result = resource_path("")
    # Should return the base path
    assert isinstance(result, str)
    assert len(result) > 0


def test_resource_path_with_nested_path():
    """Test resource_path with a nested directory path."""
    nested_path = "some/nested/directory/file.txt"
    result = resource_path(nested_path)
    assert isinstance(result, str)
    # The result should contain the nested path components
    assert "file.txt" in result


def test_resource_path_uses_meipass_when_available(monkeypatch):
    """Test that resource_path uses sys._MEIPASS when it exists (PyInstaller frozen)."""
    fake_meipass = "/tmp/fake_meipass_dir"
    monkeypatch.setattr(sys, "_MEIPASS", fake_meipass, raising=False)

    result = resource_path("test.txt")
    expected = os.path.join(fake_meipass, "test.txt")
    assert result == expected


def test_resource_path_uses_cwd_when_meipass_not_available():
    """Test that resource_path falls back to current directory when not frozen."""
    # Ensure _MEIPASS doesn't exist
    if hasattr(sys, "_MEIPASS"):
        delattr(sys, "_MEIPASS")

    result = resource_path("test.txt")
    expected = os.path.join(os.path.abspath("."), "test.txt")
    assert result == expected


def test_resource_path_handles_backslashes():
    """Test resource_path handles Windows-style backslashes."""
    result = resource_path("assets\\image.png")
    assert isinstance(result, str)
    assert "image.png" in result


def test_resource_path_absolute_base():
    """Test that the base path in the result is absolute."""
    result = resource_path("file.txt")
    # The directory part should be an absolute path
    dir_part = os.path.dirname(result)
    assert os.path.isabs(dir_part) or dir_part == ""
