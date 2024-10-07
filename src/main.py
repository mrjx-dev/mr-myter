"""
Main orchestration module for the YouTube video uploader.

This module coordinates all functions, classes, and modules required for the automated
YouTube video upload process, including browser control, file management, and user interaction.
"""

import os
import time
import traceback

from utility.driver import setup_driver, start_chrome_debugger
from utility.uploader import upload_video


def main():
    """
    Execute the main YouTube video upload process.

    This function:
    1. Initializes the Chrome driver with debugging capabilities
    2. Locates video files in the designated folder
    3. Uploads each video to YouTube sequentially
    4. Handles user input for process termination or restart
    5. Manages exceptions and performs cleanup

    The function runs in a loop, allowing for multiple upload sessions until the user chooses to exit.

    Raises:
        Exception: If there's an error during execution, particularly with driver initialization.
    """
    try:
        print("WELCOME TO YOUTUBE UPLOADER!")
        print("by: @mrjxtr")
        print(r" __    __     ______       __     __  __     ______   ______    ")
        print(r'/\ "-./  \   /\  == \     /\ \   /\_\_\_\   /\__  _\ /\  == \   ')
        print(r"\ \ \-./\ \  \ \  __<    _\_\ \  \/_/\_\/_  \/_/\ \/ \ \  __<   ")
        print(r" \ \_\ \ \_\  \ \_\ \_\ /\_____\   /\_\/\_\    \ \_\  \ \_\ \_\ ")
        print(r"  \/_/  \/_/   \/_/ /_/ \/_____/   \/_/\/_/     \/_/   \/_/ /_/ ")
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

            print("NO MORE VIDEOS TO UPLOAD.")
            print()
            print()
            time.sleep(1)
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
