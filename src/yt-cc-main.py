import os
import subprocess
import time
import traceback

import dotenv
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
dotenv.load_dotenv()

# Get the studio URL from environment variable
studio_url = os.getenv("YOUTUBE_STUDIO_URL")


def start_chrome_debugger():
    # Start Chrome with remote debugging
    command: str = r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222'

    try:
        subprocess.Popen(command, shell=True)
        print("Starting Chrome with remote debugging...")
        time.sleep(4)  # Wait for 4 seconds
    except Exception as e:
        print(f"Error starting Chrome: {str(e)}")


def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized successfully")

        # Navigate to the studio URL
        print(f"Navigating to {studio_url[:38]}...")
        driver.get(studio_url)

        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {str(e)}")
        return None


def safe_find_element(driver, by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException:
        print(f"Element not found: {by}={value}")
        return None


def safe_click(driver, element):
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def find_thumbnail(video_path):
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    for ext in [".jpg", ".jpeg", ".png", ".gif"]:
        thumbnail_path = os.path.join(video_dir, video_name + ext)
        if os.path.exists(thumbnail_path):
            return thumbnail_path
    return None


def upload_video(driver, video_path, current_video, total_videos):
    video_path = os.path.abspath(video_path)
    video_filename = os.path.basename(video_path)
    video_title = os.path.splitext(video_filename)[0]

    try:
        print(f"Video {current_video}/{total_videos}: {video_filename}")
        driver.get(studio_url)

        # Wait for the create button to be clickable
        create_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#create-icon"))
        )
        create_button.click()

        # Wait for the upload option to be clickable
        upload_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//tp-yt-paper-item[@role='menuitem']//yt-formatted-string[contains(text(), 'Upload videos')]",
                )
            )
        )
        upload_option.click()
        print("Uploading video...")

        # Wait for the file input to be present
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        file_input.send_keys(video_path)

        next_button = safe_find_element(
            driver, By.CSS_SELECTOR, "#next-button", timeout=300
        )
        if not next_button:
            raise Exception("Video upload timed out")

        time.sleep(10)

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

        upload_dialog = safe_find_element(
            driver, By.CSS_SELECTOR, "ytcp-uploads-dialog"
        )
        if upload_dialog:
            driver.execute_script("arguments[0].scrollTop += 500;", upload_dialog)
        else:
            print("Upload dialog not found for scrolling")

        time.sleep(2)  # Wait for the page to settle after scrolling

        thumbnail_path = find_thumbnail(video_path)
        if thumbnail_path:
            thumbnail_input = safe_find_element(
                driver,
                By.CSS_SELECTOR,
                'input[type="file"][accept="image/jpeg,image/png"]',
            )
            if thumbnail_input:
                thumbnail_input.send_keys(thumbnail_path)
                print("Thumbnail uploaded...")
                time.sleep(5)
                print("Processing video...")
                time.sleep(15)
            else:
                print("Thumbnail input not found")
        else:
            print("No matching thumbnail found")

        print(f"Video {current_video}/{total_videos} uploaded!...")
        print("Preparing next video...")
        print("...")
        print("...")
        driver.get(studio_url)

    except TimeoutException as te:
        print(
            f"Timeout error: {current_video}/{total_videos} - {video_filename}: {str(te)}"
        )
    except Exception as e:
        print(
            f"Error uploading video {current_video}/{total_videos} - {video_filename}: {str(e)}"
        )
        print(f"Traceback: {traceback.format_exc()}")


def main():
    try:
        print("WELCOME TO YOUTUBE UPLOADER!")
        print()
        print()
        start_chrome_debugger()
        driver = setup_driver()
        if not driver:
            raise Exception("Failed to initialize WebDriver")

        while True:  # Main loop to allow restarting
            script_dir = os.path.dirname(__file__)
            videos_folder = os.path.abspath(os.path.join(script_dir, "../videos"))
            print(
                f"Checking for videos in: ...{os.path.sep}{os.path.basename(videos_folder)}"
            )

            video_files = [
                f
                for f in os.listdir(videos_folder)
                if f.endswith((".mp4", ".avi", ".mov"))
            ]

            if not video_files:
                print("No video files found in the specified folder.")
            else:
                total_videos = len(video_files)
                print(f"Found {total_videos} video(s) to upload.")

                for index, video_file in enumerate(video_files, start=1):
                    video_path = os.path.join(videos_folder, video_file)
                    upload_video(driver, video_path, index, total_videos)
                    time.sleep(10)

            print("NO MORE VIDEOS TO UPLOAD.")
            print()
            print()
            print("YOUTUBE UPLOADER HAS FINISHED.")

            # Ask user if they want to exit or restart
            while True:
                choice = input("Do you want to exit? ([y]/n): ").lower()
                if choice in ["", "y", "yes"]:
                    print("Exiting YouTube Uploader. Goodbye!")
                    return  # Exit the function
                elif choice in ["n", "no"]:
                    restart = input(
                        "Do you want to start YouTube Uploader again? ([y]/n): "
                    ).lower()
                    if restart in ["", "y", "yes"]:
                        print("Restarting YouTube Uploader in:")
                        for i in range(3, 0, -1):
                            print(f"{i}...")
                            time.sleep(1)
                        time.sleep(1)
                        print("Restarting now!")
                        break  # Break the inner loop to restart the uploader
                    elif restart in ["n", "no"]:
                        print("Exiting YouTube Uploader in:")
                        for i in range(3, 0, -1):
                            print(f"{i}...")
                            time.sleep(1)
                        print("Goodbye!")
                        time.sleep(1)
                        return  # Exit the function
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
    finally:
        if "driver" in locals() and driver:
            driver.quit()


if __name__ == "__main__":
    main()
