"""
YouTube Video Uploader Driver Module

This module manages the Chrome WebDriver for automated YouTube video uploading. It provides:
- Functionality to start Chrome with remote debugging enabled
- Setup of the Selenium WebDriver with appropriate options
- Navigation to the YouTube Studio URL

The module utilizes Selenium WebDriver and ChromeDriverManager to interact with Chrome,
facilitating automated interactions with YouTube Studio.
"""

import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from utility.config import STUDIO_URL


def start_chrome_debugger() -> None:
    """
    Launch Chrome with remote debugging enabled.

    This function starts a new Chrome instance with a remote debugging port (9222),
    allowing Selenium to connect to an existing browser session. This approach can
    help bypass certain login requirements and browser restrictions.

    Raises:
        Exception: If there's an error starting Chrome with the debugging flag.
    """
    # Start Chrome with remote debugging
    command: str = r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222'

    try:
        subprocess.Popen(command, shell=True)
        print("Starting Chrome with remote debugging...")
    except Exception as e:
        print(f"Error starting Chrome: {str(e)}")


def setup_driver() -> WebDriver | None:
    """
    Initialize and configure the Selenium WebDriver for Chrome.

    This function:
    1. Sets up Chrome options for remote debugging
    2. Initializes the WebDriver with these options
    3. Navigates to the YouTube Studio URL

    Returns:
        WebDriver or None: Initialized WebDriver instance if successful, None if an error occurs.

    Raises:
        Exception: If there's an error during WebDriver initialization or navigation.
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized successfully")

        print(f"Navigating to {STUDIO_URL[:38]}...")
        driver.get(STUDIO_URL)

        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {str(e)}")
        return None
