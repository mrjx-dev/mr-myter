# YouTube Uploader

## Project Summary

YouTube Uploader is an automated tool for bulk video uploads to YouTube.

Key features include:

- Automated video and thumbnail uploads
- Batch processing
- Error handling and status updates
- Option to restart after completion

Using Selenium WebDriver, it simulates user actions in YouTube Studio, streamlining the upload process for content creators. This tool saves time for those who regularly upload multiple videos to YouTube.

## Prerequisites

- Python 3.10 or later
- Chrome Browser installed
- pip (Python package installer)
- Required Python packages:
  - selenium
  - python-dotenv
  - webdriver-manager
- A .env file in the project root your YOUTUBE_STUDIO_URL set

## Steps to run

1. Install Python 3.10 or later.
2. Install the required packages:

    In Powershell:

    ```powershell
    pip install selenium python-dotenv webdriver-manager
    ```

    Or

    ```powershell
    pip install -r requirements.txt
    ```

3. Create a .env file in the root of the project with the following:

    ```.env
    YOUTUBE_STUDIO_URL="https://studio.youtube.com/channel/..your-channel-id.."
    ```

4. Add the all videos and thumbnails you want to upload to the `videos` folder.

    The folder should look like this:

    ```plaintext
    youtube-uploader     <- project folder
    │ 
    ├── .env               <- environment variables
    ├── LICENCE            <- licence
    ├── README.md          <- Project README
    │ 
    ├── src                  <- source code folder
    │   └── yt-cc-main.py      <- main script
    │ 
    └── videos               <- videos folder
        ├── video1.mp4         <- your video1 file
        ├── video1.jpg         <- your thumbnail1 file
        ├── video2.mp4         <- your video2 file
        ├── video2.png         <- your thumbnail2 file
        ├── video3.mp4         <- ...
        └── ...                <- ...
    ```

5. Rename videos and their corresponding thumbnails with the same name of the title you want to give the YouTube video.
6. Navigate to the root folder of the project and start Powershell.
7. Run the following command to start the script:

    ```powershell
    python .\src\yt-cc-main.py
    ```

## Process Steps

1. Starts Chrome with remote debugging enabled.
2. Initializes the WebDriver and navigates to the YouTube Studio URL.
3. Checks for video files in the specified folder.
4. For each video file:
   a. Navigates to the YouTube Studio upload page.
   b. Clicks the "Create" button and selects "Upload videos".
   c. Uploads the video file.
   d. Renames the video with the filename (without extension).
   e. Uploads the thumbnail if a matching one is found.
   f. Waits for processing and prepares for the next video.
5. After uploading all videos, asks the user if they want to exit or restart the process.
6. If restarting, the script goes back to step 3.
7. If exiting, the script closes the WebDriver and terminates.

Note: The script handles various exceptions and provides status updates throughout the process.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Contributions are welcome! Please feel free to submit a PR.
