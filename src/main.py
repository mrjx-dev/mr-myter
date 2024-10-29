"""
Main module for Mr-Myter.

Coordinates functions and modules for automated YouTube video upload.
"""

import os
import time
import traceback

from utility import ChromeDriver, YouTubeUploader, mrjxtr


def main() -> None:
    """
    Execute YouTube video upload process.

    1. Initialize Chrome driver
    2. Locate video files
    3. Upload videos to YouTube
    4. Handle user input for termination or restart
    5. Manage exceptions and cleanup

    Raises:
        Exception: If driver initialization fails.
    """
    try:
        mrjxtr.print_intro()
        chrome_driver = ChromeDriver()
        chrome_driver.start_chrome_debugger()
        driver = chrome_driver.setup_driver()
        if not driver:
            raise Exception("Failed to initialize WebDriver")

        uploader = YouTubeUploader(driver)

        while True:
            script_dir = os.path.dirname(__file__)
            videos_folder = os.path.abspath(os.path.join(script_dir, "../videos"))
            print(
                f"Checking for videos in: ...{os.path.sep}{os.path.basename(videos_folder)}"
            )

            video_files: list[str] = [
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
                    uploader.upload_video(video_path, index, total_videos)

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
                        break  # Break the inner loop to restart
                    elif restart in ["n", "no"]:
                        print("Exiting YouTube Uploader in:")
                        for i in range(3, 0, -1):
                            print(f"{i}...")
                            time.sleep(1)
                        print("Goodbye!")
                        time.sleep(1)
                        return  # Exit
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
    finally:
        if chrome_driver:
            chrome_driver.quit_driver()


if __name__ == "__main__":
    main()
