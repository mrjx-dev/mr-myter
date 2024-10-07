"""
YouTube Video Uploader.

Manages YouTube video uploading process and interface interactions.
"""

import os
import time
import traceback

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utility.config import STUDIO_URL


class YouTubeUploader:
    def __init__(self, driver):
        self.driver = driver

    def safe_find_element(self, by, value, timeout=10) -> EC.WebElement | None:
        """
        Safely locate an element on the page.

        Args:
            by: Locator method.
            value: Locator value.
            timeout: Maximum wait time in seconds.

        Returns:
            WebElement or None: Found element or None if not found.
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"Element not found: {by}={value}")
            return None

    def safe_click(self, element) -> None:
        """
        Safely click an element, using JavaScript if needed.

        Args:
            element: Element to click.

        Raises:
            Exceptions not caught by ElementClickInterceptedException.
        """
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    @staticmethod
    def find_thumbnail(video_path: str) -> str | None:
        """
        Find matching thumbnail for a video file.

        Args:
            video_path: Path to video file.

        Returns:
            str or None: Path to thumbnail if found, None otherwise.
        """
        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        for ext in [".jpg", ".jpeg", ".png", ".gif"]:
            thumbnail_path = os.path.join(video_dir, video_name + ext)
            if os.path.exists(thumbnail_path):
                return thumbnail_path
        return None

    def navigate_to_upload_page(self) -> None:
        """
        Navigate to YouTube Studio upload page.

        Raises:
            TimeoutException: If page elements are not clickable.
        """
        self.driver.get(STUDIO_URL)
        create_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#create-icon"))
        )
        self.safe_click(create_button)

        upload_option = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//tp-yt-paper-item[@role='menuitem']//yt-formatted-string[contains(text(), 'Upload videos')]",
                )
            )
        )
        self.safe_click(upload_option)
        print("Navigated to upload page")

    def select_video_file(self, video_path) -> None:
        """
        Select video file for upload.

        Args:
            video_path: Full path to video file.

        Raises:
            TimeoutException: If file input is not present.
        """
        file_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        file_input.send_keys(video_path)
        print("Video file selected")

    def wait_for_input_fields(self) -> None:
        """
        Wait for input fields on upload dialog.

        Raises:
            Exception: If input fields don't appear within timeout.
        """
        next_button = self.safe_find_element(
            By.CSS_SELECTOR, "#next-button", timeout=300
        )
        if not next_button:
            raise Exception("Input fields not found")

    def set_video_title(self, video_title) -> None:
        """
        Set title of uploaded video.

        Args:
            video_title: Title for the video.
        """
        title_input = self.safe_find_element(
            By.CSS_SELECTOR,
            "ytcp-social-suggestions-textbox[id='title-textarea'] div[id='textbox']",
        )
        if title_input:
            title_input.clear()
            title_input.send_keys(video_title)
            print(f"Video renamed: {video_title}")
        else:
            print("Failed to rename video title")

    def scroll_upload_dialog(self) -> None:
        """
        Scroll upload dialog to reveal more options.
        """
        upload_dialog = self.safe_find_element(By.CSS_SELECTOR, "ytcp-uploads-dialog")
        if upload_dialog:
            self.driver.execute_script("arguments[0].scrollTop += 500;", upload_dialog)
        else:
            print("Upload dialog not found for scrolling")

    def upload_thumbnail(self, thumbnail_path) -> None:
        """
        Upload video thumbnail if available.

        Args:
            thumbnail_path: Path to thumbnail file or None.
        """
        if thumbnail_path:
            thumbnail_input = self.safe_find_element(
                By.CSS_SELECTOR,
                'input[type="file"][accept="image/jpeg,image/png"]',
            )
            if thumbnail_input:
                thumbnail_input.send_keys(thumbnail_path)
                print("Thumbnail uploaded...")
                time.sleep(1)
                print("Processing video...")
                time.sleep(5)
            else:
                print("Thumbnail input not found")
        else:
            print("No matching thumbnail found")

    def upload_video(self, video_path, current_video, total_videos):
        """
        Handle video upload process.

        Args:
            video_path: Full path to video file.
            current_video: Index of current video.
            total_videos: Total number of videos to upload.

        Raises:
            TimeoutException: If any upload step times out.
            Exception: For other upload errors.
        """
        video_path = os.path.abspath(video_path)
        video_filename = os.path.basename(video_path)
        video_title = os.path.splitext(video_filename)[0]

        try:
            print(f"Video {current_video}/{total_videos}: {video_filename}")

            self.navigate_to_upload_page()
            self.select_video_file(video_path)
            self.wait_for_input_fields()
            self.set_video_title(video_title)
            self.scroll_upload_dialog()

            thumbnail_path = self.find_thumbnail(video_path)
            self.upload_thumbnail(thumbnail_path)

            print(f"Video {current_video}/{total_videos} uploaded!")
            print("Preparing next video...")
            time.sleep(1)
            print("...")
            time.sleep(1)
            print("..")
            time.sleep(1)
            print(".")
            self.driver.get(STUDIO_URL)

        except TimeoutException as te:
            print(
                f"Timeout error: {current_video}/{total_videos} - {video_filename}: {str(te)}"
            )
        except Exception as e:
            print(
                f"Error uploading video {current_video}/{total_videos} - {video_filename}: {str(e)}"
            )
            print(f"Traceback: {traceback.format_exc()}")