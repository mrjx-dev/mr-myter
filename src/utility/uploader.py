"""
YouTube Video Uploader Module

This module contains functions for the YouTube video uploading process, including:
- Interacting with the YouTube Studio interface
- Handling file uploads and video details
- Managing the upload workflow

The functions use Selenium WebDriver to automate interactions with the YouTube Studio web interface.
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


def safe_find_element(driver, by, value, timeout=10) -> EC.WebElement | None:
    """
    Safely locate an element on the page, waiting for its presence.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The method used to locate the element (e.g., By.ID, By.CSS_SELECTOR).
        value (str): The locator value corresponding to the chosen method.
        timeout (int): Maximum time to wait for the element, default is 10 seconds.

    Returns:
        WebElement or None: The found element if successful, None if the element is not found within the timeout period.
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException:
        print(f"Element not found: {by}={value}")
        return None


def safe_click(driver, element) -> None:
    """
    *Attempt to safely click an element, using JavaScript if the regular click is intercepted.

    This function first tries a regular Selenium click. If that fails due to an interception,
    it falls back to a JavaScript click, which can bypass certain overlay issues.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        element (WebElement): The element to be clicked.

    Raises:
        Any exceptions not caught by the ElementClickInterceptedException handler.
    """
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def find_thumbnail(video_path: str) -> str | None:
    """
    Finds a matching thumbnail file for a given video file.

    Args:
        video_path (str): The path to the video file.

    Returns:
        str or None: The path to the thumbnail file if found, None otherwise.
    """
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    for ext in [".jpg", ".jpeg", ".png", ".gif"]:
        thumbnail_path = os.path.join(video_dir, video_name + ext)
        if os.path.exists(thumbnail_path):
            return thumbnail_path
    return None


def navigate_to_upload_page(driver) -> None:
    """
    Navigate to the YouTube Studio upload page.

    This function clicks the create button and selects the 'Upload videos' option.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Raises:
        TimeoutException: If the create button or upload option is not clickable within 20 seconds.
    """
    driver.get(STUDIO_URL)
    create_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#create-icon"))
    )
    safe_click(driver, create_button)

    upload_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//tp-yt-paper-item[@role='menuitem']//yt-formatted-string[contains(text(), 'Upload videos')]",
            )
        )
    )
    safe_click(driver, upload_option)
    print("Navigated to upload page")


def select_video_file(driver, video_path) -> None:
    """
    Select the video file for upload.

    This function locates the file input element and sends the video file path to it.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        video_path (str): The full path to the video file.

    Raises:
        TimeoutException: If the file input element is not present within 20 seconds.
    """
    file_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input.send_keys(video_path)
    print("Video file selected")


def wait_for_input_fields(driver) -> None:
    """
    Wait for the input fields on the upload dialog to appear.

    This function waits for the input fields on the upload dialog to appear before interacting with them.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Raises:
        Exception: If the input fields on the upload dialog don't appear within 300 seconds (5 minutes).
    """
    next_button = safe_find_element(
        driver, By.CSS_SELECTOR, "#next-button", timeout=300
    )
    if not next_button:
        raise Exception("Input fields not found")


def set_video_title(driver, video_title) -> None:
    """
    Set the title of the uploaded video.

    This function locates the title input field, clears it, and enters the new title.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        video_title (str): The title to set for the video.
    """
    title_input = safe_find_element(
        driver,
        By.CSS_SELECTOR,
        "ytcp-social-suggestions-textbox[id='title-textarea'] div[id='textbox']",
    )
    if title_input:
        title_input.clear()
        title_input.send_keys(video_title)
        print(f"Video renamed: {video_title}")
    else:
        print("Failed to rename video title")


def scroll_upload_dialog(driver) -> None:
    """
    Scroll the upload dialog to reveal more options.

    This function uses JavaScript to scroll the upload dialog down by 500 pixels.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    upload_dialog = safe_find_element(driver, By.CSS_SELECTOR, "ytcp-uploads-dialog")
    if upload_dialog:
        driver.execute_script("arguments[0].scrollTop += 500;", upload_dialog)
    else:
        print("Upload dialog not found for scrolling")


def upload_thumbnail(driver, thumbnail_path) -> None:
    """
    Upload a thumbnail for the video if available.

    This function locates the thumbnail input element and uploads the thumbnail if found.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        thumbnail_path (str): The path to the thumbnail file, or None if not found.
    """
    if thumbnail_path:
        thumbnail_input = safe_find_element(
            driver,
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


def upload_video(driver, video_path, current_video, total_videos):
    """
    Main function to handle the video upload process.

    This function orchestrates the entire upload process by calling other helper functions.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        video_path (str): The full path to the video file to be uploaded.
        current_video (int): The index of the current video in the upload queue.
        total_videos (int): The total number of videos to be uploaded in this session.

    Raises:
        TimeoutException: If any step in the upload process times out.
        Exception: For any other errors during the upload process.
    """
    video_path = os.path.abspath(video_path)
    video_filename = os.path.basename(video_path)
    video_title = os.path.splitext(video_filename)[0]

    try:
        print(f"Video {current_video}/{total_videos}: {video_filename}")

        navigate_to_upload_page(driver)
        select_video_file(driver, video_path)
        wait_for_input_fields(driver)
        set_video_title(driver, video_title)
        scroll_upload_dialog(driver)

        thumbnail_path = find_thumbnail(video_path)
        upload_thumbnail(driver, thumbnail_path)

        print(f"Video {current_video}/{total_videos} uploaded!")
        print("Preparing next video...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print("..")
        time.sleep(1)
        print(".")
        driver.get(STUDIO_URL)

    except TimeoutException as te:
        print(
            f"Timeout error: {current_video}/{total_videos} - {video_filename}: {str(te)}"
        )
    except Exception as e:
        print(
            f"Error uploading video {current_video}/{total_videos} - {video_filename}: {str(e)}"
        )
        print(f"Traceback: {traceback.format_exc()}")
