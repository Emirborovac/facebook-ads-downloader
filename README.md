# Video Downloader App

This Django-based web application allows users to download videos from various platforms such as YouTube, Instagram, and Facebook Ads. The application supports filtering based on the type of video source and handles errors efficiently, providing clear feedback to users.

## Features
- **YouTube Video Downloads:** Supports downloading YouTube videos with duration limits.
- **Instagram Video Downloads:** Allows users to download Instagram reels or videos.
- **Facebook Ad Video Downloads:** Provides functionality to download Facebook ad videos using a headless Chrome browser.

## Installation

Clone the repository:
```bash
git clone https://github.com/your-repo/video-downloader.git
cd video-downloader
''' 
Install dependencies: Make sure you have Python and pip installed. Install the required packages by running:


```bash
pip install -r requirements.txt
```



Set up the Django project: Run the following commands to set up the database and start the server:



python manage.py migrate
python manage.py runserver


## Usage

Navigate to the homepage: Open your browser and go to http://localhost:8000.

Download Videos: Enter the URL of the video you want to download. The app will automatically detect if the URL is from YouTube, Instagram, or Facebook Ads, and process the download accordingly.
Supported Platforms

    YouTube: Detects video URLs and downloads them if they are between 0.5 and 1200 seconds in length.
    Instagram: Downloads reels or other Instagram videos if a valid session file is available.
    Facebook Ads: Downloads Facebook ad videos using a headless Chrome browser session.

Debugging and Logging

The app prints debug information to the console for troubleshooting. In case of errors, it returns appropriate messages to the user and logs the details.