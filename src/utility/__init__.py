"""
Utility module initialization.

This module provides configuration settings, web driver setup, and YouTube video uploading functionality.
"""

from .config import STUDIO_URL
from .driver import ChromeDriver
from .uploader import YouTubeUploader

__all__: list[str] = [
    "ChromeDriver",
    "STUDIO_URL",
    "YouTubeUploader",
]
