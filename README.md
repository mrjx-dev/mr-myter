# 🤖 Mr-Myter (Automated Mass YouTube Uploader)

> ⚠ NOT ACTIVELY MAINTAINED

![Welcome-Mr-Myter](/docs/welcome-mr-myter.png)

## 📜 History

As mentioned on my GitHub profile, I am also a YouTube Content Strategist, Manager, and SEO Specialist. I found myself regularly uploading YouTube videos in bulk, scheduling them, and ensuring that everything from the titles to the descriptions and tags are perfect for SEO. To optimize my workflow and save time, I decided to put my Python programming skills to the test and created this tool. This allows me more free time to focus on creating more content and improving my strategies.

<div align="center">
  
  [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mrjxtr)
  [![Upwork](https://img.shields.io/badge/-Upwork-6fda44?style=flat-square&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/~01f2fd0e74a0c5055a?mp_source=share)
  [![Facebook](https://img.shields.io/badge/-Facebook-1877F2?style=flat-square&logo=facebook&logoColor=white)](https://www.facebook.com/mrjxtr)
  [![Instagram](https://img.shields.io/badge/-Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/mrjxtr)
  [![Threads](https://img.shields.io/badge/-Threads-000000?style=flat-square&logo=threads&logoColor=white)](https://www.threads.net/@mrjxtr)
  [![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/mrjxtr)
  [![Gmail](https://img.shields.io/badge/-Gmail-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:mr.jesterlumacad@gmail.com)

</div>

## 📝 Project Summary

Mr-MYTer is an automated tool for bulk video uploads to YouTube.

Key features include:

- Automated video and thumbnail uploads
- Automated video title and description
- Batch processing
- Error handling and status updates
- Option to restart after completion

Using Selenium WebDriver, it simulates user actions in YouTube Studio, streamlining the upload process for content creators. This tool saves time for those who regularly upload multiple videos to YouTube.

## 🛠️ Requirements

- Python 3.10 or later
- Chrome Browser installed
- pip (Python package installer)
- Required Python packages:
  - selenium
  - python-dotenv
  - webdriver-manager
- A .env file in the project root your `YOUTUBE_STUDIO_URL` set

## 🚀 Steps to run

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

   see: `.example.env`

   ```.env
   YOUTUBE_STUDIO_URL="https://studio.youtube.com/channel/..your-channel-id.."
   ```

4. Add the all videos and thumbnails you want to upload to the `videos` folder.

   The folder should look like this:

   ```plaintext
   youtube-uploader     <- project root directory
   │
   └── videos               <- videos directory
       ├── video1.mp4         <- your video1 file
       ├── video1.jpg         <- your thumbnail1 file
       ├── video2.mp4         <- your video2 file
       ├── video2.png         <- your thumbnail2 file
       ├── video3.mp4         <- ...
       └── ...                <- ...
   ```

5. Rename videos and their corresponding thumbnails with the same name of the title you want to give the YouTube video.
6. Create `.txt` files for video and name with the same name as the video titles.
7. In each `.txt` file, write down keywords/key phrases that you would like your description to have.

   The `.txt` file should look like this:

   ```plaintext
   your keyword one, your keyword 2, your keyword 3, ...
   ```

   7.2. On your YouTube studio, go to `settings`, then `upload defaults` and change the default description to something like this:

   ```plaintext
   In this video you will learn about KEYWORD. Watch the video till the end to find out KEYWORD.

   Did you learn KEYWORD? Share this video with someone who wants to see a video about KEYWORD.

   Do you want to see another video about KEYWORD?

   Did you enjoy watching TITLE?
   ```

   > Each "KEYWORD" and "TITLE" on your description will be replaced with a keyword from your `.txt` file and the title of the video respectively.

8. Navigate to the root folder of the project and start Powershell.
9. Run the following command to start the script:

   ```powershell
   python .\src\main.py
   ```

## 🔄 Process Steps

1. Starts Chrome with remote debugging enabled.
2. Initializes the WebDriver and navigates to the YouTube Studio URL.
3. Checks for video files in the specified folder.
4. For each video file:
   a. Navigates to the YouTube Studio upload page.
   b. Clicks the "Create" button and selects "Upload videos".
   c. Uploads the video file.
   d. Renames the video with the filename (without extension).
   e. Updates the video description with your keywords.
   f. Uploads the thumbnail if a matching one is found.
   g. Waits for processing and prepares for the next video.
5. After uploading all videos, asks the user if they want to exit or restart the process.
6. If restarting, the script goes back to step 3.
7. If exiting, the script closes the WebDriver and terminates.

Note: The script handles various exceptions and provides status updates throughout the process.

## 🗺 Roadmap

This will not include settings for your video uploads that you can set as default in settings > upload defaults.

Features to add:

- Auto adding tags.

- Auto setting monetization on.

- Auto uploading the video with `schedule` visibility.

- Custom path for videos and thumbnails directory/folder.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a PR.

📝 **Let's Connect!**

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mrjxtr)
[![Upwork](https://img.shields.io/badge/-Upwork-6fda44?style=flat-square&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/~01f2fd0e74a0c5055a?mp_source=share)
[![Facebook](https://img.shields.io/badge/-Facebook-1877F2?style=flat-square&logo=facebook&logoColor=white)](https://www.facebook.com/mrjxtr)
[![Instagram](https://img.shields.io/badge/-Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/mrjxtr)
[![Threads](https://img.shields.io/badge/-Threads-000000?style=flat-square&logo=threads&logoColor=white)](https://www.threads.net/@mrjxtr)
[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/mrjxtr)
[![Gmail](https://img.shields.io/badge/-Gmail-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:youremail@gmail.com)
