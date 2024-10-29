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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utility.config import STUDIO_URL


class YouTubeUploader:
    def __init__(self, driver) -> None:
        self.driver = driver

    def safe_find_element(self, by, value, timeout=10):
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

    @staticmethod
    def find_keywords(video_path: str) -> str | None:
        """
        Find matching thumbnail for a video file.

        Args:
            video_path: Path to video file.

        Returns:
            str or None: Path to thumbnail if found, None otherwise.
        """
        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        for ext in [".txt", ".md", ".json"]:
            keywords_path = os.path.join(video_dir, video_name + ext)
            if os.path.exists(keywords_path):
                return keywords_path
        return None

    @staticmethod
    def find_tags(video_path: str) -> str | None:
        """
        Find matching tags for a video file.

        Args:
            video_path: Path to video file.

        Returns:
            str or None: Path to tags file if found, None otherwise.
        """
        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        for ext in [".txt", ".md", ".json"]:
            tags_path = os.path.join(video_dir, video_name + ext)
            if os.path.exists(tags_path):
                return tags_path
        return None

    def navigate_to_upload_page(self) -> None:
        """
        Navigate to YouTube Studio upload page.

        Raises:
            TimeoutException: If page elements are not clickable.
        """
        print("\nNavigating to upload page...")
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
        time.sleep(3)

    def select_video_file(self, video_path) -> None:
        """
        Select video file for upload.

        Args:
            video_path: Full path to video file.

        Raises:
            TimeoutException: If file input is not present.
        """
        print("Selecting video to upload...")
        file_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        file_input.send_keys(video_path)
        print("Video selected!")

    def wait_for_input_fields(self) -> None:
        """
        Wait for input fields on upload dialog.

        Raises:
            Exception: If input fields don't appear within timeout.
        """
        next_button = self.safe_find_element(
            By.CSS_SELECTOR, "#next-button", timeout=300
        )
        time.sleep(3)
        if not next_button:
            raise Exception("Input fields not found")

    def set_video_title(self, video_title) -> None:
        """
        Set title of uploaded video.

        Args:
            video_title: Title for the video.
        """
        print("Renaming video title...")
        time.sleep(3)
        title_input = self.safe_find_element(
            By.CSS_SELECTOR,
            "ytcp-social-suggestions-textbox[id='title-textarea'] div[id='textbox']",
        )
        if title_input:
            title_input.clear()
            title_input.send_keys(video_title)
            print("Video renamed!")
            time.sleep(3)
        else:
            print("Failed to rename video title")

    def focus_upload_dialog(self) -> None:
        """
        Simulates a scroll on the upload dialog to focus and reveal more options.
        """
        upload_dialog = self.safe_find_element(By.CSS_SELECTOR, "ytcp-uploads-dialog")
        if upload_dialog:
            self.driver.execute_script("arguments[0].scrollTop += 500;", upload_dialog)
        else:
            print("Error: Upload dialog not found!")

    def upload_thumbnail(self, thumbnail_path) -> None:
        """
        Upload video thumbnail if available.

        Args:
            thumbnail_path: Path to thumbnail file or None.
        """
        print("Uploading thumbnail...")
        if thumbnail_path:
            thumbnail_input = self.safe_find_element(
                By.CSS_SELECTOR,
                'input[type="file"][accept="image/jpeg,image/png"]',
            )
            if thumbnail_input:
                thumbnail_input.send_keys(thumbnail_path)
                time.sleep(3)
                print("Thumbnail uploaded!")
                time.sleep(3)
            else:
                print("Error: Thumbnail input not found!")
        else:
            print("Error: No matching thumbnail found!")

    def set_video_description(self, keywords_path, video_title) -> None:
        """
        Set description of uploaded video.

        Args:
            keywords_path (_type_): Path to the file that contains keywords
            video_title (_type_): Title for the video
        """
        print("Updating video description...")
        # Read first line of keywords from file and create list of keywords
        with open(keywords_path, "r") as f:
            seo_keywords = [keyword.strip() for keyword in f.readline().split(",")]

        # Find video description input Element
        description_input = self.safe_find_element(
            By.CSS_SELECTOR,
            "ytcp-social-suggestions-textbox[id='description-textarea'] div[id='textbox']",
        )

        if description_input:
            # Get the Current description text from the input field
            description = description_input.get_attribute("innerText")

        # Replace the "KEYWORD" placeholder with the the SEO Keywords
        for keyword in seo_keywords:
            description = description.replace("KEYWORD", keyword)

        # Replace the "TITLE" placeholder with the video title
        description = description.replace("TITLE", video_title)

        if description:
            self.driver.execute_script(
                """
                arguments[0].innerText = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """,
                description_input,
                description,
            )
            print("Video description is updated")
            time.sleep(5)
        else:
            print("Error: Failed to set video description")

    def expand_more_options(self) -> None:
        """Click 'Show more' button to reveal additional options if not already expanded."""
        # Try to find the button
        show_more_button = self.safe_find_element(
            By.CSS_SELECTOR, "ytcp-button[id='toggle-button']"
        )

        if show_more_button:
            button_text = show_more_button.get_attribute("aria-label") or ""
            text_content = show_more_button.find_element(
                By.CSS_SELECTOR, ".ytcp-button-shape-impl__button-text-content"
            ).text

            if "Show more" in button_text or "Show more" in text_content:
                try:
                    self.driver.execute_script(
                        "arguments[0].click();", show_more_button
                    )
                    time.sleep(5)
                except Exception as e:
                    print(f"Error clicking show more button: {str(e)}")
            else:
                print("Options are already expanded")
        else:
            print("Error: Show more button not found!")

    # TODO: Finish writing these functions.
    def set_video_tags(self, tags_path) -> None:
        """Set video tags from file, up to YouTube's limit."""
        print("Updating video tags...")
        try:
            # Expand options first to reveal tags input
            self.expand_more_options()
            time.sleep(3)

            # Read tags from second line of file
            with open(tags_path, "r") as f:
                next(f)
                tags = f.readline()

            # Find the default tag and remove it then add it to the beginning of our tags
            default_tag_text = self.safe_find_element(
                By.CSS_SELECTOR, "ytcp-chip[id='chip-0'] #chip-text"
            )
            if default_tag_text:
                default_tag = default_tag_text.text
                delete_icon = self.safe_find_element(
                    By.CSS_SELECTOR, "ytcp-chip[id='chip-0'] #delete-icon"
                )
                if delete_icon:
                    self.safe_click(delete_icon)
                    time.sleep(1)
                    tags = f"{default_tag}, {tags}"

            # Ensure tags do not exceed 500 characters
            if len(tags) > 460:
                tags = tags[:460]

            # Find tags input using the exact selector
            tags_input = self.safe_find_element(
                By.CSS_SELECTOR,
                "input.text-input.style-scope.ytcp-chip-bar[aria-label='Tags']",
            )
            time.sleep(1)

            if not tags_input:
                print("Error: Tags input not found")
                return

            # Set value and trigger events using JavaScript
            self.driver.execute_script(
                """
                var input = arguments[0];
                input.value = arguments[1];
                input.dispatchEvent(new Event('input'));
                input.dispatchEvent(new Event('change'));
                setTimeout(() => {
                    input.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));
                    input.dispatchEvent(new KeyboardEvent('keyup', {'key': 'Enter'}));
                }, 3000);
                """,
                tags_input,
                tags,
            )
            time.sleep(2)
            tags_input.send_keys(Keys.ENTER)
            time.sleep(1)
            tags_input.send_keys(Keys.ENTER)
            tags_input.send_keys(Keys.TAB)

            print("Tags are updated!")
            time.sleep(3)

        except Exception as e:
            print(f"Error setting tags: {str(e)}")

    def set_monetization():
        pass

    def set_upload_schedule():
        pass

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
        thumbnail_path = self.find_thumbnail(video_path)
        keywords_path = self.find_keywords(video_path)
        tags_path = self.find_tags(video_path)
        try:
            print(f"\nVideo {current_video}/{total_videos}: {video_filename}")

            self.navigate_to_upload_page()
            self.select_video_file(video_path)

            self.wait_for_input_fields()

            self.set_video_title(video_title)
            self.set_video_description(keywords_path, video_title)

            self.focus_upload_dialog()

            self.upload_thumbnail(thumbnail_path)
            self.set_video_tags(tags_path)

            print(f"\nVideo {current_video}/{total_videos} uploaded!")
            time.sleep(3)
            print("Preparing next video...")
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
