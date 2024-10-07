"""
Configuration Module for YouTube Video Uploader

This module manages the configuration settings for the YouTube Video Uploader application.
It is responsible for:
- Loading environment variables from a .env file
- Providing access to the YouTube Studio URL

By using python-dotenv to load environment variables, this module ensures that sensitive
information like URLs are not hardcoded in the application, enhancing security and flexibility.
"""

import os

import dotenv

# Load environment variables
dotenv.load_dotenv()

# Get the studio URL from environment variable
STUDIO_URL: str | None = os.getenv(key="YOUTUBE_STUDIO_URL")
