"""
Chrome WebDriver management for YouTube video uploading.

Handles Chrome initialization and WebDriver setup.
"""

import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from .config import STUDIO_URL


class ChromeDriver:
    def __init__(self):
        self.driver = None

    def start_chrome_debugger(self) -> None:
        """
        Launch Chrome with remote debugging.

        Raises:
            Exception: If Chrome fails to start with debugging flag.
        """
        # Start Chrome with remote debugging
        command: str = r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222'

        try:
            subprocess.Popen(command, shell=True)
            print("Starting Chrome with remote debugging...")
        except Exception as e:
            print(f"Error starting Chrome: {str(e)}")

    def setup_driver(self) -> WebDriver | None:
        """
        Initialize and configure Selenium WebDriver.

        Returns:
            WebDriver or None: Initialized WebDriver or None if error occurs.

        Raises:
            Exception: If WebDriver initialization or navigation fails.
        """
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("WebDriver initialized successfully")

            print(f"Navigating to {STUDIO_URL[:38]}...")
            self.driver.get(STUDIO_URL)

            return self.driver
        except Exception as e:
            print(f"Error initializing WebDriver: {str(e)}")
            return None

    def get_driver(self) -> WebDriver | None:
        """
        Get current WebDriver instance.

        Returns:
            WebDriver or None: Current WebDriver instance if initialized.
        """
        return self.driver

    def quit_driver(self) -> None:
        """
        Quit WebDriver instance if it exists.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
