"""
Configuration for Mr-Myter.

Manages settings and environment variables.
"""

import os

import dotenv

# Load environment variables
dotenv.load_dotenv()

# Get the studio URL from environment variable
STUDIO_URL: str | None = os.getenv(key="YOUTUBE_STUDIO_URL")
